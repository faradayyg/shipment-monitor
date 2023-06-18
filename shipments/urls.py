from django.urls import path

from shipments.views import ShipmentInformationViewSet

urlpatterns = [
    path(
        r"<str:tracking_number>",
        ShipmentInformationViewSet.as_view(),
        name="shipment_detail_url",
    )
]
