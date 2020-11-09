import heapq
import json
import operator
import sqlite3
from datetime import datetime

from .audio_analyzer import Audio_Analyzer
from .schemas import *


class Analyzer:
    def __init__(self, streamingHistoryFiles=[]):
        """Load the data from the given StreamingHistory files into a dictionary for lookups.
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
        self._initDatabaseConnection()
        self.libraryFiles = streamingHistoryFiles
        self.library = list()
        self._fetchItemsFromLibraryFiles()
        self._audioAnalyzer = None
        return

    def getAudioAnalyzer(self):
        if not self._audioAnalyzer:
            self._audioAnalyzer = AudioAnalyzer()
        return self._audioAnalyzer

    def setAudioAnalyzer(self, audioAnalyzer):
        self._audioAnalyzer = audioAnalyzer

    def getPopularArtists(self, payload={}):
        return self._getPopular("artistName", payload=payload)

    def getPopularItems(self, payload={}):
        return self._getPopular("trackName", payload=payload)

    def getNumberOfItems(self, payload={}):
        searchSpecs, keyword, media, count, ratingCrit = self._extractSearchSpecs(
            payload
        )
        numOfItems = 0
        if count == 0:
            return 0
        for item in self.library:
            if not (
                self._itemInTimeslot(searchSpecs, item)
                and self._itemIsMedia(media, item)
                and self._itemHasKeyword(keyword, item)
            ):
                continue
            numOfItems += 1
        return numOfItems

    def getDataPerWeekday(self, dataType="number", weekdayFormat=0):
        if type(weekdayFormat) == int:
            return self._getDataPer("weekday", weekdayNumbers, dataType)
        elif type(weekdayFormat) == str:
            return self._getDataPer("weekday", weekdayNames, dataType)

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
        searchSpecs, keyword, media, count, ratingCrit = self._extractSearchSpecs(
            payload
        )

        popular = {}
        sorted_popular = []

        for item in self.library:
            if not (
                self._itemInTimeslot(searchSpecs, item)
                and self._itemIsMedia(media, item)
                and self._itemHasKeyword(keyword, item)
            ):
                continue

            popular = self._addItemToList(item, popular, key, ratingCrit)

        sorted_popular_keys = heapq.nlargest(count, popular, key=popular.get)
        sorted_popular = [(key, popular[key]) for key in sorted_popular_keys]

        return sorted_popular

    def _fetchItemsFromLibraryFiles(self):
        for fileName in self.libraryFiles:
            with open(fileName, encoding="utf-8") as jsonFile:
                tmpList = json.load(jsonFile)
                for entry in tmpList:
                    # add user as attribute
                    userName = self._getUsername(fileName)
                    entry["user"] = userName
                    entry["podcast"] = self._checkIfPodcast(entry["artistName"])

                self.library.extend(tmpList)

    def _checkIfPodcast(self, name):
        cursor = self.databaseConnection.cursor()
        cursor.execute("SELECT count(*) FROM podcasts WHERE name = ?", (name,))
        data = cursor.fetchone()[0]
        if data == 0:
            return False
        else:
            return True

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

        if "weekday" in searchSpecs:
            if not self._itemInTimeslot_Weekday(searchSpecs["weekday"], item):
                return False

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
            res = {
                "year": value == int(item["endTime"][:4]),
                "month": value == int(item["endTime"][5:7]),
                "day": value == int(item["endTime"][8:10]),
                "hour": value == int(item["endTime"][11:13]),
            }.get(spec, True)
            if not res:
                isInTimeslot = False
        return isInTimeslot

    def _itemInTimeslot_Period(self, searchSpecs, item):
        isInTimeslot = True
        startDate = datetime(
            searchSpecs["startYear"],
            searchSpecs["startMonth"],
            searchSpecs["startDay"],
            searchSpecs["startHour"],
        )
        endDate = datetime(
            searchSpecs["endYear"],
            searchSpecs["endMonth"],
            searchSpecs["endDay"],
            searchSpecs["endHour"],
        )
        if (
            datetime.fromisoformat(item["endTime"]) < startDate
            or datetime.fromisoformat(item["endTime"]) > endDate
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

    def _itemInTimeslot_Weekday(self, spec, item):
        if str == type(spec):
            spec = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6,
            }.get(spec)
        return datetime.weekday(datetime.fromisoformat(item["endTime"])) == spec

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
        keyword = "" if not "keyword" in searchSpecs else searchSpecs["keyword"]
        return (searchSpecs, keyword, media, count, ratingCrit)

    def _getListOfPossibleYears(self):
        listOfYears = []
        for item in self.library:
            year = int(item["endTime"][:4])
            if year not in listOfYears:
                listOfYears.append(year)

        return listOfYears

    def _itemHasKeyword(self, keyword, item):
        if keyword.lower() in item["artistName"].lower():
            return True
        if keyword.lower() in item["trackName"].lower():
            return True

    def _initDatabaseConnection(self):
        db_file = "./data/podcasts.db"
        try:
            self.databaseConnection = sqlite3.connect(db_file)

        except Exception as e:
            print("Error connecting to database:")
            print(e)
