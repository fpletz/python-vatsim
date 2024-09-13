import itertools
from datetime import datetime
from typing import Any, cast

import regex
from pydantic import AwareDatetime, BaseModel, HttpUrl, field_validator, model_validator


class Atis(BaseModel):
    cid: int
    name: str
    callsign: str
    frequency: str
    facility: int
    rating: int
    server: str
    visual_range: int
    atis_code: str | None
    logon_time: AwareDatetime
    last_updated: AwareDatetime
    text_atis: str | None
    runways_in_use: list[str]

    @field_validator("callsign", mode="before")
    @classmethod
    def callsign_validator(cls, v: str) -> str:
        if v.endswith("_A_ATIS"):
            return v.removesuffix("_A_ATIS")
        return v.removesuffix("_ATIS")

    @model_validator(mode="before")
    @classmethod
    def atis_validator(cls, data: dict[str, Any]) -> dict[str, Any]:
        if "text_atis" in data:
            if data["text_atis"] is not None:
                if not isinstance(data["text_atis"], str):
                    data["text_atis"] = "\n".join(cast(list[str], data["text_atis"]))

                matches = regex.search(
                    r"(RWYS|RUNWAYS?)\sIN\sUSE\s(FOR\sLANDING\s)?((?P<first>[0-9]{2}[A-Z]?)\s)+(AND\s(TAKEOFF\s)?(?P<and>[0-9]{2}[A-Z]?))?",
                    data["text_atis"],
                )
                data["runways_in_use"] = (
                    itertools.chain.from_iterable(matches.captures("first", "and"))
                    if matches is not None
                    else []
                )
            else:
                data["runways_in_use"] = []

        return data


class Controller(BaseModel):
    cid: int
    name: str
    callsign: str
    frequency: str
    facility: int
    rating: int
    server: str
    visual_range: int
    logon_time: AwareDatetime
    last_updated: AwareDatetime
    text_atis: str

    @field_validator("text_atis", mode="before")
    @classmethod
    def atis_validator(cls, v: list[str] | None) -> str:
        if v is None:
            return ""
        return "\n".join(v)


class Facility(BaseModel):
    id: int
    short: str
    long: str


class Rating(BaseModel):
    id: int
    short: str
    long: str


class PilotRating(BaseModel):
    id: int
    short_name: str
    long_name: str


class MilitaryRating(BaseModel):
    id: int
    short_name: str
    long_name: str


class FlightPlan(BaseModel):
    flight_rules: str
    aircraft: str
    aircraft_faa: str
    aircraft_short: str
    departure: str
    arrival: str
    alternate: str
    deptime: str
    enroute_time: str
    fuel_time: str
    remarks: str
    route: str
    revision_id: int
    assigned_transponder: str


class Pilot(BaseModel):
    cid: int
    name: str
    callsign: str
    server: str
    pilot_rating: int
    military_rating: int
    latitude: float
    longitude: float
    altitude: int
    groundspeed: int
    transponder: str
    heading: int
    qnh_i_hg: float
    qnh_mb: int
    flight_plan: FlightPlan | None
    logon_time: datetime
    last_updated: datetime


class Server(BaseModel):
    ident: str
    hostname_or_ip: str
    location: str
    name: str
    clients_connection_allowed: int
    client_connections_allowed: bool
    is_sweatbox: bool


class Prefile(BaseModel):
    cid: int
    name: str
    callsign: str
    flight_plan: FlightPlan
    last_updated: datetime


class General(BaseModel):
    version: int
    reload: int
    update: str
    update_timestamp: datetime
    connected_clients: int
    unique_users: int


class VatsimData(BaseModel):
    general: General
    pilots: list[Pilot]
    controllers: list[Controller]
    atis: list[Atis]
    servers: list[Server]
    prefiles: list[Prefile]
    facilities: list[Facility]
    ratings: list[Rating]
    pilot_ratings: list[PilotRating]
    military_ratings: list[MilitaryRating]


class VatsimDataEndpoints(BaseModel):
    v3: list[str]
    transceivers: list[HttpUrl]
    servers: list[HttpUrl]
    servers_sweatbox: list[HttpUrl]


class VatsimEndpoints(BaseModel):
    data: VatsimDataEndpoints
    user: list[HttpUrl]
    metar: list[HttpUrl]
