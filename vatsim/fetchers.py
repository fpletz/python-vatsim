from functools import cache
from typing import Optional

import requests

from .constants import STATUS_JSON_URL
from .types import VatsimData, VatsimEndpoints


@cache
def fetch_vatsim_endpoints(url=STATUS_JSON_URL):
    return VatsimEndpoints.model_validate_json(requests.get(url).text)


def fetch_vatsim_data(
    url: Optional[str] = None, endpoints: Optional[VatsimEndpoints] = None
):
    if url is None:
        if endpoints is None:
            endpoints = fetch_vatsim_endpoints()

        url = endpoints.data.v3[0]

    return VatsimData.model_validate_json(requests.get(url).text)
