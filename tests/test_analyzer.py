import pytest
from voluptuous import MultipleInvalid

from src.analyzer import Analyzer


def test_init_noParameters():

    exampleFile = "./data/example/testUser/StreamingHistory.json"
    numberOfItemsStreamed = 29632

    analyzer = Analyzer()
    assert exampleFile == analyzer.libraryFiles[0]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_fileSpecified():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    numberOfItemsStreamed = 5

    analyzer = Analyzer([test_file])
    assert test_file == analyzer.libraryFiles[0]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_multipleFilesSpecified():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    test_file2 = "./data/example/testUser2/StreamingHistory.json"
    numberOfItemsStreamed = 8
    streamingHistoryFiles = [test_file, test_file2]

    analyzer = Analyzer(streamingHistoryFiles=streamingHistoryFiles)
    assert test_file == analyzer.libraryFiles[0]
    assert test_file2 == analyzer.libraryFiles[1]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_checkCreationOfUserAttribute():
    test_file = "./data/example/testUser1/StreamingHistory.json"

    analyzer = Analyzer([test_file])

    assert analyzer.library[0]["user"] == "testUser1"


def test_getPopularArtist_noParameters():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    expectedPopularArtist = ("Franz Ferdinand", 2)
    analyzer = Analyzer([test_file])
    popularArtists = analyzer.getPopularArtists()

    assert expectedPopularArtist == popularArtists[0]


def test_getPopularArtist_timeParameters():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    expectedRes = [("Franz Ferdinand", 1), ("alt-J", 1), ("Left Boy", 1)]
    analyzer = Analyzer([test_file])

    res = analyzer.getPopularArtists(payload={"year": 2018, "month": 9,})
    assert expectedRes == res


def test_getPopularArtist_timeParameter_hour():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    expectedRes = [("alt-J", 1), ("Left Boy", 1)]
    analyzer = Analyzer([test_file])

    res = analyzer.getPopularArtists(payload={"hour": 10,})
    assert expectedRes == res


def test_getPopularArtist_periodParameters():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    expectedRes = [("Franz Ferdinand", 1)]
    analyzer = Analyzer([test_file])

    res = analyzer.getPopularArtists(
        payload={
            "startYear": 2018,
            "startMonth": 9,
            "startDay": 3,
            "endYear": 2018,
            "endMonth": 9,
            "endDay": 4,
        }
    )
    assert expectedRes == res


def test_getPopularArtist_daytimeParameters():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    expectedRes = [("alt-J", 1), ("Left Boy", 1)]
    analyzer = Analyzer([test_file])

    payload = {"daytime": "morning"}
    res = analyzer.getPopularArtists(payload=payload)
    assert expectedRes == res


def test_getPopularArtist_byMsPlayed():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    expectedRes = [("Almost Daily", 1045259)]
    analyzer = Analyzer([test_file])

    payload = {"ratingCrit": "time", "count": 1}
    res = analyzer.getPopularArtists(payload=payload)
    assert expectedRes == res


def test_getPopularArtist_podcast():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    expectedRes = [("Almost Daily", 1)]
    analyzer = Analyzer([test_file])

    payload = {"media": "podcast"}
    res = analyzer.getPopularArtists(payload=payload)
    assert expectedRes == res


def test_checkSchema():
    analyzer = Analyzer()
    with pytest.raises(MultipleInvalid):
        assert analyzer.getPopularArtists(payload={"startYear": 2018,})
        assert analyzer.getPopularArtists(payload={"wrongKey": 2018,})


def test_getPopularItems_noParameters():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    expectedPopularItem = (
        "Take Me Out - Live from Avatar Studios - Franz Ferdinand",
        2,
    )
    analyzer = Analyzer([test_file])
    popularItems = analyzer.getPopularItems()

    assert expectedPopularItem == popularItems[0]
