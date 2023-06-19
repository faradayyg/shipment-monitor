import dataclasses as _dc

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, serializers

from core.services import weather as _weather_service
from shipments.models import Shipment


class ShipmentInformationSerializer(serializers.ModelSerializer):
    weather_information = serializers.SerializerMethodField()

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
    serializer_class = ShipmentInformationSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="tracking_number",
                in_=openapi.IN_QUERY,
                description="Filter by tracking number",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="carrier",
                in_=openapi.IN_QUERY,
                description="Carrier short name",
                type=openapi.TYPE_STRING,
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
