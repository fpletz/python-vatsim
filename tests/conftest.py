import pathlib
import pytest


def read_file_fixture(request, fn):
    file = pathlib.Path(request.node.fspath.strpath)
    with file.with_name(fn).open() as f:
        return f.read()


@pytest.fixture
def status_json(request):
    return read_file_fixture(request, "status.json")
