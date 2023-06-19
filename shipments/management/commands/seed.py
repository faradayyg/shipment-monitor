import csv
from typing import Any
from typing.io import TextIO

from django.core.management.base import BaseCommand
from django.db import transaction

from shipments.models import Shipment


class TableNotEmptyError(Exception):
    """Raised when target table is not empty"""


class InvalidFormatError(Exception):
    """Raised when the csv format is invalid."""


class Command(BaseCommand):
    required_csv_keys = {
        "tracking_number",
        "carrier",
        "sender_address",
        "receiver_address",
        "article_name",
        "article_quantity",
        "article_price",
        "SKU",
        "status",
    }

    def _extract_data_to_seed(self, row: dict) -> dict:
        built_dict = {}
        for key in self.required_csv_keys:
            built_dict[key] = row[key]
        return built_dict

    def _validate_csv_format(self, file: TextIO):
        reader = csv.reader(file)
        head = next(reader)
        if self.required_csv_keys.intersection(set(head)) != self.required_csv_keys:
            raise InvalidFormatError
        file.seek(0)

    @staticmethod
    def _ensure_table_is_empty():
        if Shipment.objects.first():
            raise TableNotEmptyError

    def handle(self, *args: Any, **options: Any) -> None:
        try:
            self._ensure_table_is_empty()
        except TableNotEmptyError:
            pass

        with open("shipments/seed_data.csv", "r") as csv_file, transaction.atomic():
            self._validate_csv_format(csv_file)
            reader = csv.DictReader(csv_file)
            for row in reader:
                Shipment.objects.create(**self._extract_data_to_seed(row))
