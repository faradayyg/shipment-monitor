import pytest as _pytest
from django.test import override_settings as _override_settings

import core.services.weather as _core_weather
import core.services.weather.providers as _weather_providers


@_pytest.mark.parametrize(
    "provider_setting,expected_provider",
    (
        ["open_weather_map", _weather_providers.OpenWeatherMap],
        ["weather_bit", _weather_providers.WeatherBit],
    ),
)
def test_weather_provider_depends_on_settings(provider_setting, expected_provider):
    with _override_settings(WEATHER_INFO_PROVIDER=provider_setting):
        weather_provider = _core_weather.WeatherInformationService()
        assert isinstance(weather_provider.get_provider(), expected_provider)
