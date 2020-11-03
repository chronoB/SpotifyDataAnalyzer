from .test_analyzer import analyzer_TestUser1, analyzer_TestUser2


def test_getNumberOfItems_noParameters(analyzer_TestUser1, analyzer_TestUser2):
    analyzer = analyzer_TestUser1
    analyzer2 = analyzer_TestUser2

    expectedNumber = 5
    expectedNumber2 = 3

    assert expectedNumber == analyzer.getNumberOfItems()
    assert expectedNumber2 == analyzer2.getNumberOfItems()


def test_getNumberOfItems_mediaSpecified(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedNumberOverall = 5
    expectedNumberMusic = 4
    expectedNumberPodcast = 1

    assert expectedNumberOverall == analyzer.getNumberOfItems(payload={"media": "all"})
    assert expectedNumberMusic == analyzer.getNumberOfItems(payload={"media": "music"})
    assert expectedNumberPodcast == analyzer.getNumberOfItems(
        payload={"media": "podcast"}
    )


def test_getNumberOfItems_timeSpecified(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedNumber = 3

    assert expectedNumber == analyzer.getNumberOfItems(
        payload={
            "year": 2018,
            "month": 9,
        }
    )


def test_getNumberOfItems_periodSpecified(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedNumber = 1

    payload = {
        "startYear": 2018,
        "startMonth": 9,
        "startDay": 3,
        "startHour": 0,
        "endYear": 2018,
        "endMonth": 9,
        "endDay": 4,
        "endHour": 0,
    }
    assert expectedNumber == analyzer.getNumberOfItems(payload=payload)


def test_getNumberOfItems_ratingCritSpecified(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    res1 = analyzer.getNumberOfItems(payload={"ratingCrit": "clicks"})
    res2 = analyzer.getNumberOfItems(payload={"ratingCrit": "time"})
    assert res1 == res2


def test_getNumberOfItems_countSpecified(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    res1 = analyzer.getNumberOfItems(payload={"count": 5})
    res2 = analyzer.getNumberOfItems(payload={"count": 7})
    res3 = analyzer.getNumberOfItems(payload={"count": 0})
    assert res1 == res2
    assert res3 == 0
