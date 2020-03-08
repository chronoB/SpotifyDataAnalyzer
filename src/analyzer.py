import json


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
            streamingHistoryFiles = [
                "./data/example/testUser/StreamingHistory.json"
            ]
        self.libraryFiles = streamingHistoryFiles
        self.library = dict()
        self._fetchItemsFromLibraryFiles()
        return

    def getGeneralInformation(self):
        return

    def getPopularArtist(self):
        return

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
                # turn list into dict
                for i in range(len(tmpList)):
                    # make keys out of artist and trackname
                    key = (
                        tmpList[i]["artistName"]
                        + "_"
                        + tmpList[i]["trackName"]
                    )
                    value = tmpList[i]

                    # add user as attribute
                    userName = self._getUsername(fileName)
                    value["user"] = userName

                    # handle case that song was played multiple times
                    # add a counter at the end of the key
                    # I did not use a random number to make lookups in dict easily possible if i don't care about how often it exists
                    if key in self.library:
                        counter = 1
                        key += "_" + str(counter)
                        while key in self.library:
                            counter += 1
                            key = key[: key.rfind("_")] + "_" + str(counter)

                    self.library.update({key: value})

    def _getUsername(self, fileName):
        # Returns the username from a given filename
        def getNthSlash(n):
            if n == 0:
                return 0
            return fileName.find("/", getNthSlash(n - 1)) + 1

        idxOfSlash = getNthSlash(3)
        return fileName[idxOfSlash : fileName.rfind("/")]
