from typing import Mapping, Union

from src.analyzer import Analyzer


def main() -> None:
    analyzer = Analyzer(["./data/example/testUser/StreamingHistory.json"])
    payload: Mapping[str, Union[str, int]] = {}

    print("Example 1: getPopularArtists()")
    pa = analyzer.getPopularArtists()
    print(pa)

    print()
    print("Example 1a: getPopularArtists() with specific Daytime")
    payload = {"daytime": "morning"}
    pa = analyzer.getPopularArtists(payload=payload)
    print(pa)

    print()
    print("Example 1b: getPopularArtists() of Month July")
    payload = {"month": 7}
    pa = analyzer.getPopularArtists(payload=payload)
    print(pa)

    print()
    print("Example 1c: getPopularArtists() of Month July for podcasts")
    payload = {"month": 7, "media": "podcast"}
    pa = analyzer.getPopularArtists(payload=payload)
    print(pa)

    print()
    print(
        "Example 1d: getPopularArtists() of specified period (2019-03-03 to 2019-03-04) for music, count = 3"
    )
    payload = {
        "startYear": 2019,
        "startMonth": 3,
        "startDay": 3,
        "startHour": 0,
        "endYear": 2019,
        "endMonth": 3,
        "endDay": 4,
        "endHour": 0,
        "count": 3,
        "media": "music",
    }
    pa = analyzer.getPopularArtists(payload=payload)
    print(pa)

    print()
    print("Example 1e: getPopularArtists() for specific weekday (monday)")
    payload = {
        "weekday": "monday",
    }
    pa = analyzer.getPopularArtists(payload=payload)
    print(pa)

    print()
    print("Example 2: getPopularItems()")
    pi = analyzer.getPopularItems()
    print(pi)

    print()
    print("Example 2a: getPopularItems() for podcasts")
    payload = {
        "media": "podcast",
    }
    pi = analyzer.getPopularItems(payload=payload)
    print(pi)

    print()
    print("Example 2b: getPopularItems() for podcasts by time played in ms")
    payload = {
        "media": "podcast",
        "ratingCrit": "time",
    }
    pi = analyzer.getPopularItems(payload=payload)
    print(pi)

    print()
    print("Example 2c: getPopularItems() with keyword 'franz ferdinand'")
    pi = analyzer.getPopularItems(payload={"keyword": "Franz Ferdinand"})
    print(pi)

    print()
    print("Example 2c2: getPopularItems() with keyword 'acoustic'")
    pi = analyzer.getPopularItems(payload={"keyword": "acoustic"})
    print(pi)

    print()
    print("Example 3: getDataPerWeekday()")
    dpw = analyzer.getDataPerWeekday()
    print(dpw)

    print()
    print("Example 3a: getDataPerWeekday() with string as key")
    dpw = analyzer.getDataPerWeekday(weekdayFormat="")
    print(dpw)


if __name__ == "__main__":
    main()
