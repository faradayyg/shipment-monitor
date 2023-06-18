import dataclasses as _dc

from rest_framework import generics, serializers
from rest_framework.request import Request
from rest_framework.response import Response

from core.services import weather as _weather_service
from shipments.models import Shipment


class ShipmentInformationSerializer(serializers.ModelSerializer):
    weather_information = serializers.SerializerMethodField()

    def _extract_location_data_from_address(self, address: str):
        return address.split(",")[1].strip().split(" ")[0]

    def get_weather_information(self, instance: Shipment) -> dict:
        location = _weather_service.LocationDTO.from_address(instance.receiver_address)
        return _dc.asdict(
            _weather_service.WeatherInformationService.fetch_location_weather_info(
                location
            )
        )

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


class ShipmentInformationViewSet(generics.ListAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentInformationSerializer
    filter_param: str

    def filter_queryset(self, queryset):
        filtered = super().filter_queryset(queryset)
        return filtered.filter(tracking_number=self.filter_param)

    def get(self, request: Request, tracking_number: str) -> Response:
        self.filter_param = tracking_number
        return super().get(self, request, tracking_number=tracking_number)
