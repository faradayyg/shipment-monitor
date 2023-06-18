from django.conf import settings as _settings
from django.core import cache as _dj_cache

import core.services.weather.providers as _providers

from .common import LocationDTO, WeatherInformationDTO


class WeatherInformationService:
    @staticmethod
    def get_provider():
        settings_provider_map = {
            "open_weather_map": _providers.OpenWeatherMap,
            "weather_bit": _providers.WeatherBit,
        }
        return settings_provider_map.get(
            _settings.WEATHER_INFO_PROVIDER, _providers.OpenWeatherMap
        )()

    @classmethod
    def fetch_location_weather_info(
        cls, location: LocationDTO
    ) -> WeatherInformationDTO:
        provider = cls.get_provider()
        cache_key = (
            f"{provider.cache_prefix}_weather_{location.zip}_{location.country_code}"
        )
        if weather_info := _dj_cache.cache.get(cache_key):
            return weather_info

        weather_info = provider.fetch_location_weather_info(location=location)
        _dj_cache.cache.set(cache_key, weather_info, 3600 * 2)
        return weather_info


__all__ = ["WeatherInformationService", "WeatherInformationDTO", "LocationDTO"]
