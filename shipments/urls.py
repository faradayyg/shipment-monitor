from django.urls import path

from shipments.views import ShipmentInformationViewSet

urlpatterns = [
    path(
        r"shipments/",
        ShipmentInformationViewSet.as_view(),
        name="shipment_detail_url",
    )
]
