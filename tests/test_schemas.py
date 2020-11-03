import pytest
from voluptuous import MultipleInvalid

from src.schemas import *


def test_wrongKeys():
    with pytest.raises(MultipleInvalid):
        assert SearchSpecifics(
            {
                "startYear": 2018,
            }
        )
        assert SearchSpecifics(
            {
                "wrongKey": 2018,
            }
        )


def test_weekday():
    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    for day in weekdays:
        assert SearchSpecifics(
            {
                "weekday": day,
            }
        )
    for x in range(0, 7):
        assert SearchSpecifics(
            {
                "weekday": x,
            }
        )
