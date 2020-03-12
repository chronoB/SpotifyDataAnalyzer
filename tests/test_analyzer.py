import pytest
from voluptuous import MultipleInvalid

from src.analyzer import Analyzer


@pytest.fixture
def analyzer_TestUser():
    test_file = "./data/example/testUser/StreamingHistory.json"
    return Analyzer([test_file])


@pytest.fixture
def analyzer_TestUser1():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    return Analyzer([test_file])


@pytest.fixture
def analyzer_TestUser2():
    test_file = "./data/example/testUser2/StreamingHistory.json"
    return Analyzer([test_file])


def test_checkSchema():
    analyzer = Analyzer()
    with pytest.raises(MultipleInvalid):
        assert analyzer.getPopularArtists(payload={"startYear": 2018,})
        assert analyzer.getPopularArtists(payload={"wrongKey": 2018,})


def test_init_noParameters():
    exampleFile = "./data/example/testUser/StreamingHistory.json"
    analyzer = Analyzer()

    numberOfItemsStreamed = 29632

    assert exampleFile == analyzer.libraryFiles[0]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_fileSpecified(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    numberOfItemsStreamed = 5
    test_file = "./data/example/testUser1/StreamingHistory.json"

    assert test_file == analyzer.libraryFiles[0]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_checkPodcastLabel(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    numberOfItemsStreamed = 5

    assert analyzer.library[0]["podcast"] == False
    assert analyzer.library[4]["podcast"] == True


def test_init_multipleFilesSpecified():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    test_file2 = "./data/example/testUser2/StreamingHistory.json"
    streamingHistoryFiles = [test_file, test_file2]
    analyzer = Analyzer(streamingHistoryFiles=streamingHistoryFiles)

    numberOfItemsStreamed = 8

    assert test_file == analyzer.libraryFiles[0]
    assert test_file2 == analyzer.libraryFiles[1]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_checkCreationOfUserAttribute(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    assert analyzer.library[0]["user"] == "testUser1"
