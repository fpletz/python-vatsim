import pytest
from pydantic import ValidationError

from vatsim.types import Atis, VatsimData, VatsimEndpoints


def test_fails_on_wrong_data():
    with pytest.raises(ValidationError):
        VatsimData.model_validate_json('{"foo":"bar"}')


def test_validates_status_json(status_json: str):
    VatsimEndpoints.model_validate_json(status_json)


def test_atis_validate_runways_in_use():
    atis_data = {
        "cid": 23,
        "name": "Frank Nord",
        "callsign": "ZZZZ_ATIS",
        "frequency": "122.800",
        "facility": 1,
        "rating": 1,
        "server": "unkown",
        "visual_range": 100,
        "atis_code": "Z",
        "logon_time": "2032-04-20T04:20:00+0000",
        "last_updated": "2032-04-20T04:20:00+0000",
        "text_atis": None,
    }
    atis_no_text = Atis.model_validate(atis_data)
    assert len(atis_no_text.runways_in_use) == 0

    atis_data["text_atis"] = "RUNWAYS IN USE 26L AND 26R"
    atis_with_text = Atis.model_validate(atis_data)
    assert set(atis_with_text.runways_in_use) == {"26L", "26R"}

    atis_data["callsign"] = "ZZZZ_A_ATIS"
    atis_arrival = Atis.model_validate(atis_data)
    assert atis_arrival.callsign == "ZZZZ"
