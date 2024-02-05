import pytest
from pydantic import ValidationError

from vatsim.types import VatsimData, VatsimEndpoints


def test_fails_on_wrong_data():
    with pytest.raises(ValidationError):
        VatsimData.model_validate_json('{"foo":"bar"}')


def test_validates_status_json(status_json: str):
    VatsimEndpoints.model_validate_json(status_json)
