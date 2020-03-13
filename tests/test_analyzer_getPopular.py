from .test_analyzer import analyzer_TestUser1


def test_getPopularArtist_noParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedPopularArtist = ("Franz Ferdinand", 2)

    popularArtists = analyzer.getPopularArtists()
    assert expectedPopularArtist == popularArtists[0]


def test_getPopularArtist_timeParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedRes = [("Franz Ferdinand", 1), ("alt-J", 1), ("Left Boy", 1)]

    res = analyzer.getPopularArtists(payload={"year": 2018, "month": 9,})
    assert expectedRes == res


def test_getPopularArtist_timeParameter_hour(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedRes = [("alt-J", 1), ("Left Boy", 1)]

    res = analyzer.getPopularArtists(payload={"hour": 10,})
    assert expectedRes == res


def test_getPopularArtist_timeAndMedia(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedRes = [("alt-J", 1), ("Left Boy", 1)]

    res = analyzer.getPopularArtists(payload={"hour": 10, "media": "music"})
    assert expectedRes == res


def test_getPopularArtist_periodParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedRes = [("Franz Ferdinand", 1)]

    res = analyzer.getPopularArtists(
        payload={
            "startYear": 2018,
            "startMonth": 9,
            "startDay": 3,
            "startHour": 0,
            "endYear": 2018,
            "endMonth": 9,
            "endDay": 4,
            "endHour": 0,
        }
    )
    assert expectedRes == res


def test_getPopularArtist_daytimeParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedRes = [("alt-J", 1), ("Left Boy", 1)]

    payload = {"daytime": "morning"}
    res = analyzer.getPopularArtists(payload=payload)
    assert expectedRes == res


def test_getPopularArtist_byMsPlayed(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedRes = [("Almost Daily", 1045259)]

    payload = {"ratingCrit": "time", "count": 1}
    res = analyzer.getPopularArtists(payload=payload)
    assert expectedRes == res


def test_getPopularArtist_podcast(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedRes = [("Almost Daily", 1)]

    payload = {"media": "podcast"}
    res = analyzer.getPopularArtists(payload=payload)
    assert expectedRes == res


def test_getPopularItems_noParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedPopularItem = (
        "Take Me Out - Live from Avatar Studios - Franz Ferdinand",
        2,
    )

    popularItems = analyzer.getPopularItems()
    assert expectedPopularItem == popularItems[0]


def test_getPopularItems_Weekday(analyzer_TestUser1):
    analyzer = analyzer_TestUser1
    expectedPopularItem = [
        ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1,)
    ]
    popularItems = analyzer.getPopularItems(payload={"weekday": 0})
    assert expectedPopularItem == popularItems


def test_getPopularItems_count(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    popularItems = analyzer.getPopularItems(payload={"count": 1})
    assert len(popularItems) == 1
