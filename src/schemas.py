from voluptuous import Any, In, Required, Schema

TimeSchema = Schema({"year": int, "month": int, "day": int, "hour": int,})

PeriodSchema = Schema(
    {
        Required("startYear"): int,
        Required("startMonth"): int,
        Required("startDay"): int,
        Required("endYear"): int,
        Required("endMonth"): int,
        Required("endDay"): int,
    }
)

daytimeList = ["night", "morning", "afternoon", "evening"]
Daytime = In(daytimeList)
DaytimeSchema = Schema({"daytime": Daytime,})
Media = In(["music", "podcast", "all"])

RatingCriterium = In(["clicks", "time"])

Standard = {
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
