from pathlib import Path

import pytest
from _pytest.fixtures import FixtureRequest


def read_file_fixture(request: FixtureRequest, fn: str):
    file = Path(request.node.fspath.strpath)  # pyright: ignore

    return file.with_name(fn).read_text(encoding="utf-8")


@pytest.fixture
def status_json(request: pytest.FixtureRequest):
    return read_file_fixture(request, "status.json")
