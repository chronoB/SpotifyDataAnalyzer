import heapq
import json
from datetime import datetime
from os import listdir
from os.path import isfile, join
from typing import Dict, List, Mapping, Sequence, Tuple, Union

from .schemas import *


class ExtendedAnalyzer:
    def __init__(self, streamingHistoryFiles: List[str] = []) -> None:
        """Load the data from the given extended StreamingHistory files into a dictionary for lookups.

        Example of default value:
        {
            "ts": "2018-03-08T14:14:40Z",
            "username": "dullikop",
            "platform": "Android OS 7.0 API 24 (LGE, LG-H850)",
            "ms_played": 0,
            "conn_country": "DE",
            "ip_addr_decrypted": "89.15.238.115",
            "user_agent_decrypted": "unknown",
            "master_metadata_track_name": "Into the Wild",
            "master_metadata_album_artist_name": "BOY",
            "master_metadata_album_album_name": "We Were Here",
            "spotify_track_uri": "spotify:track:1RHTNaMZrN8EwnuBmJmcRd",
            "episode_name": null,
            "episode_show_name": null,
            "spotify_episode_uri": null,
            "reason_start": "fwdbtn",
            "reason_end": "fwdbtn",
            "shuffle": true,
            "skipped": null,
            "offline": false,
            "offline_timestamp": 1520518477608,
            "incognito_mode": false
        }

        Args:
            libraryFiles ([String]): The files that contain the StreamingHistory that should be analyzed. Default is the example StreamingHistory.

        """
        if streamingHistoryFiles == []:
            streamingHistoryFiles = ["./data/example/testUser/StreamingHistory.json"]

        self.libraryFiles = []
        for entry in streamingHistoryFiles:
            # check if entry is a file
            if isfile(entry):
                self.libraryFiles.append(entry)
            else:
                self.libraryFiles.extend(
                    [join(entry, f) for f in listdir(entry) if isfile(join(entry, f))]
                )
        self.library: List[Dict[str, str]] = list()
        self._fetchItemsFromLibraryFiles()
        return

    def _fetchItemsFromLibraryFiles(self) -> None:
        for fileName in self.libraryFiles:
            with open(fileName, encoding="utf-8") as jsonFile:
                tmpList = json.load(jsonFile)
                self.library.extend(tmpList)

    def getNumOfSongsPlayed(self) -> int:
        return len(self.library)

    def getPopularArtists(
        self, payload: Mapping[str, Union[int, str]] = {}
    ) -> List[Tuple[str, int]]:
        return self._getPopular("master_metadata_album_artist_name", payload=payload)

    def getPopularItems(
        self, payload: Mapping[str, Union[int, str]] = {}
    ) -> List[Tuple[str, int]]:
        return self._getPopular("master_metadata_track_name", payload=payload)

    def getPopularPodcast(
        self, payload: Mapping[str, Union[int, str]] = {}
    ) -> List[Tuple[str, int]]:
        return self._getPopular("episode_show_name", payload=payload)

    def getPopularPodcastItems(
        self, payload: Mapping[str, Union[int, str]] = {}
    ) -> List[Tuple[str, int]]:
        return self._getPopular("episode_name", payload=payload)

    def getNumberOfItems(self, payload: Mapping[str, Union[int, str]] = {}) -> int:
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

    def getDataPerWeekday(
        self, dataType: str = "number", weekdayFormat: Union[int, str] = 0
    ) -> Dict[Union[str, int], object]:
        if isinstance(weekdayFormat, int):
            return self._getDataPer("weekday", weekdayNumbers, dataType)
        elif isinstance(weekdayFormat, str):
            return self._getDataPer("weekday", weekdayNames, dataType)
        else:
            raise Exception("weekdayFormat is not of type int or str")

    def getDataPerDayTime(
        self, dataType: str = "number"
    ) -> Dict[Union[str, int], object]:
        return self._getDataPer("daytime", daytimeList, dataType)

    def getDataPerYear(self, dataType: str = "number") -> Dict[Union[str, int], object]:
        yearList: List[int] = self._getListOfPossibleYears()
        return self._getDataPer("year", yearList, dataType)

    def getDataPerMonth(
        self, dataType: str = "number"
    ) -> Dict[Union[str, int], object]:
        monthList: List[int] = [x for x in range(1, 13)]
        return self._getDataPer("month", monthList, dataType)

    def getDataPerDay(self, dataType: str = "number") -> Dict[Union[str, int], object]:
        dayList: List[int] = [x for x in range(1, 32)]
        return self._getDataPer("day", dayList, dataType)

    def _getDataPer(
        self, key: str, timeList: Sequence[Union[str, int]], dataType: str
    ) -> Dict[Union[str, int], object]:
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

    def _getPopular(
        self, key: str, payload: Mapping[str, Union[int, str]] = {}
    ) -> List[Tuple[str, int]]:
        searchSpecs, keyword, media, count, ratingCrit = self._extractSearchSpecs(
            payload
        )

        popular: Dict[str, int] = {}
        sorted_popular: List[Tuple[str, int]] = []

        for item in self.library:
            if not (
                self._itemInTimeslot(searchSpecs, item)
                and self._itemIsMedia(media, item)
                and self._itemHasKeyword(keyword, item)
            ):
                continue

            popular = self._addItemToList(item, popular, key, ratingCrit)

        sorted_popular_keys = heapq.nlargest(count, popular, key=popular.get)  # type: ignore
        sorted_popular = [(key, popular[key]) for key in sorted_popular_keys]

        return sorted_popular

    def _extractSearchSpecs(
        self, payload: Mapping[str, Union[int, str]]
    ) -> Tuple[Dict[str, int], str, str, int, str]:
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

    def _itemInTimeslot(
        self, searchSpecs: SearchSpecifics, item: Dict[str, str]  # type: ignore
    ) -> int:
        if searchSpecs == {}:
            return 1

        if "weekday" in searchSpecs:
            if not self._itemInTimeslot_Weekday(searchSpecs["weekday"], item):
                return 0

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
            return 1

    def _itemInTimeslot_Time(
        self, searchSpecs: SearchSpecifics, item: Dict[str, str]  # type: ignore
    ) -> int:
        isInTimeslot = 1

        for spec, value in searchSpecs.items():
            res = {
                "year": value == int(item["ts"][:4]),
                "month": value == int(item["ts"][5:7]),
                "day": value == int(item["ts"][8:10]),
                "hour": value == int(item["ts"][11:13]),
            }.get(spec, 1)
            if not res:
                isInTimeslot = 0
        return isInTimeslot

    def _itemInTimeslot_Period(
        self, searchSpecs: SearchSpecifics, item: Dict[str, str]  # type: ignore
    ) -> int:
        isInTimeslot = 1
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
            datetime.fromisoformat(item["ts"][:-1]) < startDate
            or datetime.fromisoformat(item["ts"][:-1]) > endDate
        ):
            isInTimeslot = 0

        return isInTimeslot

    def _itemInTimeslot_Daytime(self, spec: str, item: Dict[str, str]) -> int:
        hour = int(item["ts"][11:13])
        return {
            "night": hour >= 0 and hour < 6,
            "morning": hour >= 6 and hour < 12,
            "afternoon": hour >= 12 and hour < 18,
            "evening": hour >= 18 and hour <= 23,
        }.get(spec, 0)

    def _itemInTimeslot_Weekday(
        self, spec: Union[str, int], item: Dict[str, str]
    ) -> int:

        if isinstance(spec, str):
            intSpec = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6,
            }.get(spec)
        elif isinstance(spec, int):
            intSpec = spec
        return datetime.weekday(datetime.fromisoformat(item["ts"][:-1])) == intSpec

    def _itemIsMedia(self, media: str, item: Dict[str, str]) -> int:
        isMedia = {
            "all": 1,
            "podcast": 1 if item["episode_show_name"] else 0,
            "music": 0 if item["episode_show_name"] else 1,
        }.get(media, 0)
        return isMedia

    def _itemHasKeyword(self, keyword: str, item: Dict[str, str]) -> int:

        # Check because there is some data missing/corrupted data
        if (
            not item["master_metadata_album_artist_name"]
            and not item["episode_show_name"]
        ):
            return 0

        if item["master_metadata_album_artist_name"]:
            if (
                keyword.lower() in item["master_metadata_album_artist_name"].lower()
                or keyword.lower() in item["master_metadata_track_name"].lower()
            ):
                return 1
        elif item["episode_show_name"]:
            if (
                keyword.lower() in item["episode_show_name"].lower()
                or keyword.lower() in item["episode_name"].lower()
            ):
                return 1
        return 0

    def _addItemToList(
        self,
        item: Dict[str, str],
        usedDict: Dict[str, int],
        key: str,
        ratingCrit: Union[str, int],
    ) -> Dict[str, int]:
        if item[key]:
            if key == "master_metadata_album_artist_name":
                if item[key] not in usedDict.keys():
                    usedDict[item[key]] = (
                        1 if ratingCrit == "clicks" else int(item["ms_played"])
                    )
                else:
                    usedDict[item[key]] += (
                        1 if ratingCrit == "clicks" else int(item["ms_played"])
                    )
            elif key == "master_metadata_track_name":
                # when the popularItems should be returned they should be returned with "master_metadata_track_name - master_metadata_album_artist_name"

                extendedKey = (
                    item["master_metadata_track_name"]
                    + " - "
                    + item["master_metadata_album_artist_name"]
                )
                if extendedKey not in usedDict.keys():
                    usedDict[extendedKey] = (
                        1 if ratingCrit == "clicks" else int(item["ms_played"])
                    )
                else:
                    usedDict[extendedKey] += (
                        1 if ratingCrit == "clicks" else int(item["ms_played"])
                    )
            elif key == "episode_name":
                # when the popularItems should be returned they should be returned with "episode_name - episode_show_name"
                extendedKey = item["episode_name"] + " - " + item["episode_show_name"]
                if extendedKey not in usedDict.keys():
                    usedDict[extendedKey] = (
                        1 if ratingCrit == "clicks" else int(item["ms_played"])
                    )
                else:
                    usedDict[extendedKey] += (
                        1 if ratingCrit == "clicks" else int(item["ms_played"])
                    )
            elif key == "episode_show_name":
                if item[key] not in usedDict.keys():
                    usedDict[item[key]] = (
                        1 if ratingCrit == "clicks" else int(item["ms_played"])
                    )
                else:
                    usedDict[item[key]] += (
                        1 if ratingCrit == "clicks" else int(item["ms_played"])
                    )
        return usedDict

    def _getListOfPossibleYears(self) -> List[int]:
        listOfYears = []
        for item in self.library:
            year = int(item["endTime"][:4])
            if year not in listOfYears:
                listOfYears.append(year)
        return listOfYears
