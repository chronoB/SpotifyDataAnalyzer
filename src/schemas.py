from voluptuous import Any, In, Required, Schema

TimeSchema = Schema({"year": int, "month": int, "day": int, "hour": int,})

PeriodSchema = Schema(
    {
        Required("startYear"): int,
        Required("startMonth"): int,
        Required("startDay"): int,
        Required("startHour"): int,
        Required("endYear"): int,
        Required("endMonth"): int,
        Required("endDay"): int,
        Required("endHour"): int,
    }
)

daytimeList = ["night", "morning", "afternoon", "evening"]
Daytime = In(daytimeList)
DaytimeSchema = Schema({"daytime": Daytime,})

Media = In(["music", "podcast", "all"])

RatingCriterium = In(["clicks", "time"])

Weekday = In(
    [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        0,
        1,
        2,
        3,
        4,
        5,
        6,
    ]
)
weekdayNumbers = [0, 1, 2, 3, 4, 5, 6]
weekdayNames = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

Standard = {
    "keyword": str,
    "weekday": Weekday,
    "media": Media,
    "count": int,
    "ratingCrit": RatingCriterium,
}

SearchSpecifics = Any(
    TimeSchema.extend(Standard),
    PeriodSchema.extend(Standard),
    DaytimeSchema.extend(Standard),
    Schema(Standard),
)

DataType = In(["number", "artist", "item"])
