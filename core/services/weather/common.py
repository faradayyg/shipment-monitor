import dataclasses as _dc
from abc import abstractmethod

import pycountry as _pycountry


@_dc.dataclass
class LocationDTO:
    zip: str
    country_code: str

    @classmethod
    def from_address(cls, address: str):
        country = address.split(",")[2].strip()
        zip_code = address.split(",")[1].strip().split(" ")[0]
        return cls(
            zip=zip_code, country_code=_pycountry.countries.lookup(country).alpha_2
        )


@_dc.dataclass
class WeatherInformationDTO:
    weather: str
    weather_description: str
    temperature: float
    feels_like: float
    max_temperature: float
    min_temperature: float
    humidity: int
    visibility: int


class WeatherInformationBaseClass:
    cache_prefix: str

    @abstractmethod
    def fetch_location_weather_info(
        self, location: LocationDTO
    ) -> WeatherInformationDTO:
        raise NotImplementedError("Please implement this method")
