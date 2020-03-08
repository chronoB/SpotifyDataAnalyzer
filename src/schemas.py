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

DaytimeSchema = In(["night", "morning", "afternoon", "evening"])

Media = In(["music", "podcast", "all"])

SearchSpecifics = Any(TimeSchema, PeriodSchema, DaytimeSchema, Schema({}))
