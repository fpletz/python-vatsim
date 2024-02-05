from typing import cast

from pydantic.networks import HttpUrl

STATUS_JSON_URL: HttpUrl = cast(HttpUrl, "https://status.vatsim.net/status.json")
