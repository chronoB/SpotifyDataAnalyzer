from .test_analyzer import analyzer_TestUser1


def test_getDataPerDaytime_noParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {"night": 1, "morning": 2, "afternoon": 1, "evening": 1}

    assert expectedResult == analyzer.getDataPerDayTime()


def test_getDataPerDaytime_number(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {"night": 1, "morning": 2, "afternoon": 1, "evening": 1}

    assert expectedResult == analyzer.getDataPerDayTime("number")


def test_getDataPerDaytime_artists(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {
        "night": [("Franz Ferdinand", 1)],
        "morning": [("alt-J", 1), ("Left Boy", 1)],
        "afternoon": [("Almost Daily", 1)],
        "evening": [("Franz Ferdinand", 1)],
    }

    assert expectedResult == analyzer.getDataPerDayTime("artist")


def test_getDataPerDaytime_item(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {
        "night": [("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1)],
        "morning": [("Tessellate - alt-J", 1), ("The Return of... - Left Boy", 1)],
        "afternoon": [("Fragen aus der Community - Almost Daily", 1)],
        "evening": [("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1)],
    }

    assert expectedResult == analyzer.getDataPerDayTime("item")


def test_getDataPerYear_noParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {
        2018: 3,
        2019: 2,
    }

    assert expectedResult == analyzer.getDataPerYear()


def test_getDataPerYear_number(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {
        2018: 3,
        2019: 2,
    }

    assert expectedResult == analyzer.getDataPerYear("number")


def test_getDataPerYear_artists(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {
        2018: [("Franz Ferdinand", 1), ("alt-J", 1), ("Left Boy", 1)],
        2019: [("Franz Ferdinand", 1), ("Almost Daily", 1)],
    }

    assert expectedResult == analyzer.getDataPerYear("artist")


def test_getDataPerYear_item(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {
        2018: [
            ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1),
            ("Tessellate - alt-J", 1),
            ("The Return of... - Left Boy", 1),
        ],
        2019: [
            ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1),
            ("Fragen aus der Community - Almost Daily", 1),
        ],
    }

    assert expectedResult == analyzer.getDataPerYear("item")


def test_getDataPerMonth_noParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {
        1: 2,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 3,
        10: 0,
        11: 0,
        12: 0,
    }

    assert expectedResult == analyzer.getDataPerMonth()


def test_getDataPerMonth_number(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {
        1: 2,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 3,
        10: 0,
        11: 0,
        12: 0,
    }

    assert expectedResult == analyzer.getDataPerMonth("number")


def test_getDataPerMonth_artists(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for month in range(1, 13):
        expectedResult[month] = []
    expectedResult[1] = [("Franz Ferdinand", 1), ("Almost Daily", 1)]
    expectedResult[9] = [("Franz Ferdinand", 1), ("alt-J", 1), ("Left Boy", 1)]

    assert expectedResult == analyzer.getDataPerMonth("artist")


def test_getDataPerMonth_item(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for month in range(1, 13):
        expectedResult[month] = []
    expectedResult[1] = [
        ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1),
        ("Fragen aus der Community - Almost Daily", 1),
    ]
    expectedResult[9] = [
        ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1),
        ("Tessellate - alt-J", 1),
        ("The Return of... - Left Boy", 1),
    ]

    assert expectedResult == analyzer.getDataPerMonth("item")


def test_getDataPerDay_noParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in range(1, 32):
        expectedResult[day] = 0
    expectedResult[1] = 1
    expectedResult[3] = 1
    expectedResult[8] = 1
    expectedResult[15] = 2

    assert expectedResult == analyzer.getDataPerDay()


def test_getDataPerDay_number(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in range(1, 32):
        expectedResult[day] = 0
    expectedResult[1] = 1
    expectedResult[3] = 1
    expectedResult[8] = 1
    expectedResult[15] = 2

    assert expectedResult == analyzer.getDataPerDay("number")


def test_getDataPerDay_artists(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in range(1, 32):
        expectedResult[day] = []
    expectedResult[1] = [("Franz Ferdinand", 1)]
    expectedResult[3] = [("Franz Ferdinand", 1)]
    expectedResult[8] = [("Almost Daily", 1)]
    expectedResult[15] = [("alt-J", 1), ("Left Boy", 1)]

    assert expectedResult == analyzer.getDataPerDay("artist")


def test_getDataPerDay_item(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in range(1, 32):
        expectedResult[day] = []
    expectedResult[1] = [
        ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1)
    ]
    expectedResult[3] = [
        ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1)
    ]
    expectedResult[8] = [("Fragen aus der Community - Almost Daily", 1)]
    expectedResult[15] = [("Tessellate - alt-J", 1), ("The Return of... - Left Boy", 1)]

    assert expectedResult == analyzer.getDataPerDay("item")


def test_getDataPerWeekday_noParameters(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in range(0, 7):
        expectedResult[day] = 0
    expectedResult[0] = 1
    expectedResult[1] = 2
    expectedResult[5] = 2

    assert expectedResult == analyzer.getDataPerWeekday()


def test_getDataPerWeekday_number(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in range(0, 7):
        expectedResult[day] = 0
    expectedResult[0] = 1
    expectedResult[1] = 2
    expectedResult[5] = 2

    assert expectedResult == analyzer.getDataPerWeekday("number")


def test_getDataPerWeekday_artists(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in range(0, 7):
        expectedResult[day] = []
    expectedResult[0] = [("Franz Ferdinand", 1)]
    expectedResult[1] = [("Franz Ferdinand", 1), ("Almost Daily", 1)]
    expectedResult[5] = [("alt-J", 1), ("Left Boy", 1)]

    assert expectedResult == analyzer.getDataPerWeekday("artist",)


def test_getDataPerWeekday_item(analyzer_TestUser1):
    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in range(0, 7):
        expectedResult[day] = []
    expectedResult[0] = [
        ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1)
    ]
    expectedResult[1] = [
        ("Take Me Out - Live from Avatar Studios - Franz Ferdinand", 1),
        ("Fragen aus der Community - Almost Daily", 1),
    ]
    expectedResult[5] = [("Tessellate - alt-J", 1), ("The Return of... - Left Boy", 1)]

    assert expectedResult == analyzer.getDataPerWeekday("item")


def test_getDataPerWeekday_weekdayFormat(analyzer_TestUser1):
    from src.schemas import weekdayNames

    analyzer = analyzer_TestUser1

    expectedResult = {}
    for day in weekdayNames:
        expectedResult[day] = 0
    expectedResult["monday"] = 1
    expectedResult["tuesday"] = 2
    expectedResult["saturday"] = 2

    assert expectedResult == analyzer.getDataPerWeekday(weekdayFormat=str())
