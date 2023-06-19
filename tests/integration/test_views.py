import dataclasses as _dc
import decimal as _decimal
import unittest.mock as _mock

import django.urls as _urls
import factory as _factory
import pytest as _pytest
import rest_framework.test as _drf_test

import core.services.weather as _weather_service
import shipments.models as _models


class ShipmentFactory(_factory.django.DjangoModelFactory):
    class Meta:
        model = _models.Shipment


@_pytest.fixture
def api_client() -> _drf_test.APIClient:
    return _drf_test.APIClient()


@_pytest.fixture
def weather_information() -> _weather_service.WeatherInformationDTO:
    return _weather_service.WeatherInformationDTO(
        weather="sunny",
        weather_description="Always in philly",
        temperature=22.5,
        feels_like=30.0,
        max_temperature=25.5,
        min_temperature=19.0,
        humidity=200,
        visibility=90,
    )


@_pytest.fixture(autouse=True)
def shipment() -> _models.Shipment:
    return ShipmentFactory(
        tracking_number="AABB",
        article_quantity=1,
        article_price=_decimal.Decimal(200),
        carrier="DHL",
        sender_address="Street 1, 10115 Berlin, Germany",
        receiver_address="Street 1, 10115 Berlin, Germany",
    )


class TestShipmentListView:
    url = _urls.reverse("shipment_detail_url")

    @_pytest.mark.django_db
    @_mock.patch.object(
        _weather_service.WeatherInformationService, "fetch_location_weather_info"
    )
    def test_api_response_structure(
        self, mocked_weather_fetch, api_client, weather_information
    ):
        mocked_weather_fetch.return_value = weather_information
        res = api_client.get(f"{self.url}?tracking_number=AABB")
        assert res.status_code == 200
        assert res.data[0]["weather_information"] == _dc.asdict(weather_information)
        assert set(res.data[0].keys()) == {
            "id",
            "tracking_number",
            "carrier",
            "sender_address",
            "receiver_address",
            "article_name",
            "article_quantity",
            "article_price",
            "SKU",
            "status",
            "weather_information",
        }

    @_pytest.mark.django_db
    @_mock.patch.object(
        _weather_service.WeatherInformationService, "fetch_location_weather_info"
    )
    def test_filter_by_tracking_number(self, mocked_weather_fetch, api_client):
        res = api_client.get(f"{self.url}?tracking_number=SOME_RUBBISH")
        assert res.status_code == 200
        assert len(res.data) == 0

    @_pytest.mark.django_db
    @_mock.patch.object(
        _weather_service.WeatherInformationService, "fetch_location_weather_info"
    )
    def test_filter_by_shipment_carrier(
        self, mocked_weather_fetch, api_client, weather_information, shipment
    ):
        mocked_weather_fetch.return_value = weather_information
        shipment.carrier = "DHL"
        shipment.save()
        res = api_client.get(f"{self.url}?carrier=DHL")
        assert res.status_code == 200
        assert len(res.data) == 1

    @_pytest.mark.django_db
    @_mock.patch.object(
        _weather_service.WeatherInformationService, "fetch_location_weather_info"
    )
    def test_filter_by_carrier_and_tracking_number(
        self, mocked_weather_fetch, api_client, weather_information, shipment
    ):
        ShipmentFactory(
            tracking_number="AABB",
            article_quantity=1,
            article_price=_decimal.Decimal(200),
            carrier="NOT_DHL",
            sender_address="Street 1, 10115 Berlin, Germany",
            receiver_address="Street 1, 10115 Berlin, Germany",
        )
        mocked_weather_fetch.return_value = weather_information
        shipment.carrier = "DHL"
        shipment.save()
        res = api_client.get(f"{self.url}?carrier=DHL&tracking_number=AABB")
        assert res.status_code == 200
        assert len(res.data) == 1

    @_pytest.mark.django_db
    def test_api_request_calls_service(self, api_client, weather_information):
        with _mock.patch.object(
            _weather_service.WeatherInformationService,
            "fetch_location_weather_info",
            return_value=weather_information,
        ) as mocked_service:
            res = api_client.get(f"{self.url}?tracking_number=AABB")

        mocked_service.assert_called_once()
        assert res.status_code == 200
