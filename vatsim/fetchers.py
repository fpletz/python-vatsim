from functools import cache

import requests
from pydantic import HttpUrl

from .constants import STATUS_JSON_URL
from .types import VatsimData, VatsimEndpoints


@cache
def fetch_vatsim_endpoints(url: HttpUrl = STATUS_JSON_URL):
    return VatsimEndpoints.model_validate_json(requests.get(str(url)).text)


def fetch_vatsim_data(url: str | None = None, endpoints: VatsimEndpoints | None = None):
    if url is None:
        if endpoints is None:
            endpoints = fetch_vatsim_endpoints()

        url = endpoints.data.v3[0]

    return VatsimData.model_validate_json(requests.get(url).text)
