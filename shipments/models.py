import django.db.models as _models
from django.utils.translation import gettext_lazy as _


class Carriers(_models.TextChoices):
    DHL = "DHL", _("shipments.enums.carrier.dhl")
    DPD = "DPD", _("shipments.enums.carrier.dpd")
    GLS = "GLS", _("shipments.enums.carrier.gls")
    UPS = "UPS", _("shipments.enums.carrier.ups")
    FEDEX = "FDX", _("shipments.enums.carrier.fedex")


class Shipment(_models.Model):
    tracking_number = _models.CharField(max_length=50)
    carrier = _models.CharField(max_length=6, choices=Carriers.choices)
    sender_address = _models.CharField(max_length=200)
    receiver_address = _models.CharField(max_length=200)
    article_name = _models.CharField(max_length=120)
    article_quantity = _models.IntegerField()
    article_price = _models.DecimalField(max_digits=12, decimal_places=4)
    SKU = _models.CharField(max_length=50)
    status = _models.CharField(max_length=20)
