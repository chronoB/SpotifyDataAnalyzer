import heapq
import json
import operator

from .schemas import *


class Analyzer:
    def __init__(self, streamingHistoryFiles=[]):
        """ Load the data from the given StreamingHistory files into a dictionary for lookups.
        Every item will have an extra "user"-feature added that contains the name of the folder where the StreamingHistory is located.
        Example of default value:
        {
            "endTime" : "2018-09-03 20:39",
            "artistName" : "Franz Ferdinand",
            "trackName" : "Take Me Out - Live from Avatar Studios",
            "msPlayed" : 207997,
            "user": "example"
        }

        Args:
            libraryFiles ([String]): The files that contain the StreamingHistory that should be analyzed. Default is the example StreamingHistory.

        """
        if streamingHistoryFiles == []:
            streamingHistoryFiles = ["./data/example/testUser/StreamingHistory.json"]
        self.libraryFiles = streamingHistoryFiles
        self.podcastList = dict()
        self._fetchPodcastsFromFile()
        self.library = list()
        self._fetchItemsFromLibraryFiles()
        return

    def getGeneralInformation(self):
        return

    def getPopularArtists(self, payload={}):
        return self._getPopular("artistName", payload=payload)

    def getPopularItems(self, payload={}):
        return self._getPopular("trackName", payload=payload)

    def getNumberOfItems(self, payload={}):
        searchSpecs, media, count, ratingCrit = self._extractSearchSpecs(payload)
        numOfItems = 0
        if count == 0:
            return 0
        for item in self.library:
            if not (
                self._itemInTimeslot(searchSpecs, item)
                and self._itemIsMedia(media, item)
            ):
                continue
            numOfItems += 1
        return numOfItems

    def getDataPerDayTime(self, dataType="number"):
        return self._getDataPer("daytime", daytimeList, dataType)

    def getDataPerYear(self, dataType="number"):
        yearList = self._getListOfPossibleYears()
        return self._getDataPer("year", yearList, dataType)

    def getDataPerMonth(self, dataType="number"):
        monthList = [x for x in range(1, 13)]
        return self._getDataPer("month", monthList, dataType)

    def getDataPerDay(self, dataType="number"):
        dayList = [x for x in range(1, 32)]
        return self._getDataPer("day", dayList, dataType)

    def _getDataPer(self, key, timeList, dataType):
        dt = DataType(dataType)
        retDict = {}
        for time in timeList:
            data = {
                "number": self.getNumberOfItems(payload={key: time}),
                "artist": self.getPopularArtists(payload={key: time}),
                "item": self.getPopularItems(payload={key: time}),
            }.get(dt, [])
            retDict[time] = data
        return retDict

    def _getPopular(self, key, payload={}):
        searchSpecs, media, count, ratingCrit = self._extractSearchSpecs(payload)

        popular = {}
        sorted_popular = []

        for item in self.library:
            if not (
                self._itemInTimeslot(searchSpecs, item)
                and self._itemIsMedia(media, item)
            ):
                continue

            popular = self._addItemToList(item, popular, key, ratingCrit)

        sorted_popular_keys = heapq.nlargest(count, popular, key=popular.get)
        sorted_popular = [(key, popular[key]) for key in sorted_popular_keys]

        if count < len(sorted_popular):
            return sorted_popular[:count]
        else:
            return sorted_popular

    def _fetchItemsFromLibraryFiles(self):
        for fileName in self.libraryFiles:
            with open(fileName, encoding="utf-8") as jsonFile:
                tmpList = json.load(jsonFile)
                for entry in tmpList:
                    # add user as attribute
                    userName = self._getUsername(fileName)
                    entry["user"] = userName
                    entry["podcast"] = (
                        True if entry["artistName"] in self.podcastList else False
                    )

                self.library.extend(tmpList)

    def _getUsername(self, fileName):
        # Returns the username from a given filename
        def getNthSlash(n):
            if n == 0:
                return 0
            return fileName.find("/", getNthSlash(n - 1)) + 1

        idxOfSlash = getNthSlash(3)
        return fileName[idxOfSlash : fileName.rfind("/")]

    def _itemInTimeslot(self, searchSpecs, item):
        if searchSpecs == {}:
            return True

        if "daytime" in searchSpecs:
            return self._itemInTimeslot_Daytime(searchSpecs["daytime"], item)

        elif "endYear" in searchSpecs:
            # endYear is required for a Period Schema
            return self._itemInTimeslot_Period(searchSpecs, item)

        elif (
            "year" in searchSpecs
            or "month" in searchSpecs
            or "day" in searchSpecs
            or "hour" in searchSpecs
        ):
            return self._itemInTimeslot_Time(searchSpecs, item)

        else:
            return True

    def _itemInTimeslot_Time(self, searchSpecs, item):
        isInTimeslot = True

        for spec, value in searchSpecs.items():
            if spec not in ["year", "month", "day", "hour"]:
                continue
            res = {
                "year": value == int(item["endTime"][:4]),
                "month": value == int(item["endTime"][5:7]),
                "day": value == int(item["endTime"][8:10]),
                "hour": value == int(item["endTime"][11:13]),
            }.get(spec, False)
            if not res:
                isInTimeslot = False
        return isInTimeslot

    def _itemInTimeslot_Period(self, searchSpecs, item):
        isInTimeslot = True
        itemYear = int(item["endTime"][:4])
        itemMonth = int(item["endTime"][5:7])
        itemDay = int(item["endTime"][8:10])

        if (
            searchSpecs["startYear"] > itemYear
            or searchSpecs["endYear"] < itemYear
            or searchSpecs["startMonth"] < itemMonth
            or searchSpecs["endMonth"] < itemMonth
            or searchSpecs["startDay"] < itemDay
            or searchSpecs["startMonth"] < itemDay
        ):
            isInTimeslot = False

        return isInTimeslot

    def _itemInTimeslot_Daytime(self, spec, item):
        hour = int(item["endTime"][11:13])
        return {
            "night": hour >= 0 and hour < 6,
            "morning": hour >= 6 and hour < 12,
            "afternoon": hour >= 12 and hour < 18,
            "evening": hour >= 18 and hour <= 23,
        }.get(spec, False)

    def _itemIsMedia(self, media, item):
        return {
            "all": True,
            "podcast": item["podcast"],
            "music": not item["podcast"],
        }.get(media, False)

    def _addItemToList(self, item, usedDict, key, ratingCrit):
        if key == "artistName":
            if item[key] not in usedDict.keys():
                usedDict[item[key]] = 1 if ratingCrit == "clicks" else item["msPlayed"]
            else:
                usedDict[item[key]] += 1 if ratingCrit == "clicks" else item["msPlayed"]
        elif key == "trackName":
            # when the popularItems should be returned they should be returned with "trackName - artistName"
            extendedKey = item["trackName"] + " - " + item["artistName"]
            if extendedKey not in usedDict.keys():
                usedDict[extendedKey] = (
                    1 if ratingCrit == "clicks" else item["msPlayed"]
                )
            else:
                usedDict[extendedKey] += (
                    1 if ratingCrit == "clicks" else item["msPlayed"]
                )
        return usedDict

    def _fetchPodcastsFromFile(self):
        with open("data/podcastFile.txt", encoding="utf-8") as podcastFile:
            self.podcastList = podcastFile.read().splitlines()

    def _extractSearchSpecs(self, payload):
        searchSpecs = SearchSpecifics(payload)
        media = (
            Media("all") if not "media" in searchSpecs else Media(searchSpecs["media"])
        )
        count = 5 if not "count" in searchSpecs else searchSpecs["count"]
        ratingCrit = (
            RatingCriterium("clicks")
            if not "ratingCrit" in searchSpecs
            else RatingCriterium(searchSpecs["ratingCrit"])
        )
        return (searchSpecs, media, count, ratingCrit)

    def _getListOfPossibleYears(self):
        listOfYears = []
        for item in self.library:
            year = int(item["endTime"][:4])
            if year not in listOfYears:
                listOfYears.append(year)

        return listOfYears
