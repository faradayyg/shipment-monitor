import requests as _requests
import structlog as _logging
from django.conf import settings as _settings
from django.core import cache as _dj_cache

import core.services.weather.common as _weather_commons

_logger = _logging.get_logger(__name__)


class OpenWeatherMapFetchException(Exception):
    """Raised when fetching from OWM fails."""


class OpenWeatherMap(_weather_commons.WeatherInformationBaseClass):
    base_url: str = "https://api.openweathermap.org/"
    cache_prefix = "OWM"

    def fetch_coordinates_from_location(
        self,
        location: _weather_commons.LocationDTO,
    ) -> tuple[float, float]:
        cache_key: str = f"zip_{location.zip}_{location.country_code}"
        # Location exists in cache, return and move on
        if coordinates_from_cache := _dj_cache.cache.get(cache_key):
            return coordinates_from_cache

        try:
            url: str = (
                f"{self.base_url}geo/1.0/zip?zip={location.zip},"
                f"{location.country_code}&"
                f"appid={_settings.OPEN_WEATHER_MAP_KEY}"
            )
            res = _requests.get(url)
            if res.status_code != 200:
                _logger.error(
                    "Failed to fetch zip code information",
                    url=url,
                    location=location,
                )
                raise OpenWeatherMapFetchException("Error fetching location data")
        except _requests.exceptions.RequestException as e:
            raise OpenWeatherMapFetchException from e

        coordinates = (res.json()["lat"], res.json()["lon"])
        _dj_cache.cache.set(cache_key, coordinates, timeout=None)
        return coordinates

    def fetch_location_weather_info(
        self, location: _weather_commons.LocationDTO
    ) -> _weather_commons.WeatherInformationDTO:
        lat, lon = self.fetch_coordinates_from_location(location)
        url: str = (
            f"{self.base_url}data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={_settings.OPEN_WEATHER_MAP_KEY}"
        )

        try:
            res = _requests.get(url)
        except _requests.exceptions.RequestException as e:
            raise OpenWeatherMapFetchException from e

        if res.status_code != 200:
            _logger.error(
                "Could not fetch weather information at location",
                location=location,
                response=res.content,
            )
            raise OpenWeatherMapFetchException(
                "Could not fetch weather information at location"
            )

        weather_information = res.json()

        return _weather_commons.WeatherInformationDTO(
            weather=weather_information["weather"][0]["main"],
            weather_description=weather_information["weather"][0]["description"],
            feels_like=weather_information["main"]["feels_like"],
            humidity=weather_information["main"]["humidity"],
            visibility=weather_information["visibility"],
            temperature=weather_information["main"]["temp"],
            max_temperature=weather_information["main"]["temp_max"],
            min_temperature=weather_information["main"]["temp_min"],
        )
