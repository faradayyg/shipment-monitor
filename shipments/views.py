import dataclasses as _dc

import rest_framework as _drf
from drf_yasg import openapi as _openapi
from drf_yasg.utils import swagger_auto_schema as _swagger_auto_schema
from rest_framework import generics as _generics

import core.services.shipment as _shipment_service
from core.services import weather as _weather_service
from shipments.models import Shipment


class ShipmentInformationSerializer(_drf.serializers.ModelSerializer):
    weather_information = _drf.serializers.SerializerMethodField()
    status = _drf.serializers.SerializerMethodField()

    def get_weather_information(self, instance: Shipment) -> dict:
        location = _weather_service.LocationDTO.from_address(instance.receiver_address)
        return _dc.asdict(
            _weather_service.WeatherInformationService.fetch_location_weather_info(
                location
            )
        )

    def get_status(self, instance: Shipment) -> str:
        return _shipment_service.standardise_shipment_status_codes(instance.status)

    class Meta:
        model = Shipment
        fields = (
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
        )


class ShipmentInformationViewSet(_generics.ListAPIView):
    serializer_class = ShipmentInformationSerializer

    @_swagger_auto_schema(
        manual_parameters=[
            _openapi.Parameter(
                name="tracking_number",
                in_=_openapi.IN_QUERY,
                description="Filter by tracking number",
                type=_openapi.TYPE_STRING,
            ),
            _openapi.Parameter(
                name="carrier",
                in_=_openapi.IN_QUERY,
                description="Carrier short name",
                type=_openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Shipment.objects.all()
        tracking_number = self.request.query_params.get("tracking_number")
        carrier = self.request.query_params.get("carrier")

        if tracking_number:
            queryset = queryset.filter(tracking_number=tracking_number)
        if carrier:
            queryset = queryset.filter(carrier=carrier)
        return queryset
