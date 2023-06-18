import core.services.weather.common as _weather_commons


class WeatherBit(_weather_commons.WeatherInformationBaseClass):
    cache_prefix = "WTB"

    def fetch_location_weather_info(
        self,
        location: _weather_commons.LocationDTO,
    ) -> _weather_commons.WeatherInformationDTO:
        pass
