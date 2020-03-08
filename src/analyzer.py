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
        self.library = list()
        self._fetchItemsFromLibraryFiles()
        self.podcastList = dict()
        self._fetchPodcastsFromFile()
        return

    def getGeneralInformation(self):
        return

    def getPopularArtist(self, count=5, media="all", payload={}):
        searchSpecs = SearchSpecifics(payload)
        popularArtists = {}
        sorted_popularArtists = []
        for item in self.library:
            if not self._itemInTimeslot(searchSpecs, item) or not self._itemIsMedia(
                media, item
            ):
                continue

            key = "artistName"
            popularArtists = self._addItemToList(item, popularArtists, key)

            sorted_popularArtists = sorted(
                popularArtists.items(), key=operator.itemgetter(1), reverse=True,
            )
        if count < len(sorted_popularArtists):
            return sorted_popularArtists[:count]
        else:
            return sorted_popularArtists

    def getPopularItem(self):
        return

    def getNumberOfItems(self):
        return

    def getNumberOfItemsPerDayTime(self):
        return

    def getNumberOfItemsPerYear(self):
        return

    def getNumberOfItemsPerMonth(self):
        return

    def getNumberOfItemsPerDay(self):
        return

    def _fetchItemsFromLibraryFiles(self):
        for fileName in self.libraryFiles:
            with open(fileName, encoding="utf-8") as jsonFile:
                tmpList = json.load(jsonFile)
                for entry in tmpList:
                    # add user as attribute
                    userName = self._getUsername(fileName)
                    entry["user"] = userName
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

        daytime = ["night", "morning", "afternoon", "evening"]
        if searchSpecs in daytime:
            return self._itemInTimeslot_Daytime(searchSpecs, item)

        elif "endYear" in searchSpecs:
            # endYear is required for a Period Schema
            return self._itemInTimeslot_Period(searchSpecs, item)
        else:
            return self._itemInTimeslot_Time(searchSpecs, item)

    def _itemInTimeslot_Time(self, searchSpecs, item):
        isInTimeslot = True
        counter = 0
        for spec, value in searchSpecs.items():
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

    def _itemInTimeslot_Daytime(self, searchSpecs, item):
        hour = int(item["endTime"][11:13])
        return {
            "night": hour >= 0 and hour < 6,
            "morning": hour >= 6 and hour < 12,
            "afternoon": hour >= 12 and hour < 18,
            "night": hour >= 18 and hour <= 23,
        }.get(searchSpecs, False)

    def _itemIsMedia(self, media, item):
        return {
            "all": True,
            "podcast": item["artistName"] in self.podcastList,
            "music": item["artistName"] not in self.podcastList,
        }.get(media, False)

    def _addItemToList(self, item, usedDict, key):
        if item[key] not in usedDict.keys():
            usedDict[item[key]] = 1
        else:
            usedDict[item[key]] += 1
        return usedDict

    def _fetchPodcastsFromFile(self):
        with open("data/podcastFile.txt", encoding="utf-8") as podcastFile:
            self.podcastList = podcastFile.readlines()
