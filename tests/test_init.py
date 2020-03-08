from src.analyzer import Analyzer


def test_init_noParameters():

    exampleFile = "./data/example/testUser/StreamingHistory.json"
    numberOfItemsStreamed = 29632

    analyzer = Analyzer()
    assert exampleFile == analyzer.libraryFiles[0]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_fileSpecified():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    numberOfItemsStreamed = 4

    analyzer = Analyzer([test_file])
    assert test_file == analyzer.libraryFiles[0]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_multipleFilesSpecified():
    test_file = "./data/example/testUser1/StreamingHistory.json"
    test_file2 = "./data/example/testUser2/StreamingHistory.json"
    numberOfItemsStreamed = 7
    streamingHistoryFiles = [test_file, test_file2]

    analyzer = Analyzer(streamingHistoryFiles=streamingHistoryFiles)
    assert test_file == analyzer.libraryFiles[0]
    assert test_file2 == analyzer.libraryFiles[1]
    assert numberOfItemsStreamed == len(analyzer.library)


def test_init_library():
    test_file = "./data/example/testUser1/StreamingHistory.json"

    analyzer = Analyzer([test_file])
    itemName = "Franz Ferdinand_Take Me Out - Live from Avatar Studios"
    itemName1 = "Franz Ferdinand_Take Me Out - Live from Avatar Studios_1"

    assert itemName in analyzer.library
    assert itemName1 in analyzer.library
    assert analyzer.library[itemName1]["user"] == "testUser1"
    assert analyzer.library[itemName1]["artistName"] == "Franz Ferdinand"
    assert (
        analyzer.library[itemName1]["trackName"]
        == "Take Me Out - Live from Avatar Studios"
    )
    assert analyzer.library[itemName1]["endTime"] == "2019-01-01 00:01"
    assert analyzer.library[itemName1]["msPlayed"] == 1
