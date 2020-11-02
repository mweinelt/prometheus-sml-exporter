import asyncio
import logging

from prometheus_client import Gauge
from sml import SmlGetListResponse, SmlSequence

__version__ = "0.1.3"

logger = logging.getLogger(__name__)

OBIS = {
    "1-0:1.8.0*255": (
        Gauge,
        "smartmeter_wirkarbeit_verbrauch_total_wh",
        "Summe Wirkarbeit Verbrauch über alle Tarife",
    ),
    "1-0:1.8.1*255": (
        Gauge,
        "smartmeter_wirkarbeit_verbrauch_tarif1_wh",
        "Summe Wirkarbeit Verbrauch im Tarif 1",
    ),
    "1-0:1.8.2*255": (
        Gauge,
        "smartmeter_wirkarbeit_verbrauch_tarif2_wh",
        "Summe Wirkarbeit Verbrauch im Tarif 2",
    ),
    "1-0:1.8.3*255": (
        Gauge,
        "smartmeter_wirkarbeit_verbrauch_tarif3_wh",
        "Summe Wirkarbeit Verbrauch im Tarif 3",
    ),
    "1-0:2.8.0*255": (
        Gauge,
        "smartmeter_wirkarbeit_lieferung_total_wh",
        "Summe Wirkarbeit Lieferung über alle Tarife",
    ),
    "1-0:2.8.1*255": (
        Gauge,
        "smartmeter_wirkarbeit_lieferung_tarif1_wh",
        "Summe Wirkarbeit Lieferung im Tarif 1",
    ),
    "1-0:2.8.2*255": (
        Gauge,
        "smartmeter_wirkarbeit_lieferung_tarif2_wh",
        "Summe Wirkarbeit Lieferung im Tarif 2",
    ),
    "1-0:2.8.3*255": (
        Gauge,
        "smartmeter_wirkarbeit_lieferung_tarif3_wh",
        "Summe Wirkarbeit Lieferung im Tarif 3",
    ),
    "1-0:16.7.0*255": (Gauge, "smartmeter_wirkleistung_w", "Momentane Wirkleistung"),
}


class SmlExporter:
    def __init__(self):
        self.device = None
        self.vendor = None
        self.metrics = {}

    def get_metric(self, obis_id):
        # skip until we have seen vendor and device identifier, so we can populate the according labels
        if not self.device or not self.vendor:
            return

        if obis_id in self.metrics:
            return self.metrics[obis_id]

        try:
            _type, name, desc = OBIS[obis_id]
        except KeyError:
            logging.warning("Unhandled OBIS ID: %s", obis_id)
            raise KeyError

        metric = _type(name, f"{desc} ({obis_id})", ["vendor", "device"])
        self.metrics[obis_id] = metric

        return metric

    def event(self, message_body: SmlSequence) -> None:
        assert isinstance(message_body, SmlGetListResponse)
        for val in message_body.get("valList", []):
            obis_id = val.get("objName")

            # device id
            if obis_id == "1-0:0.0.9*255":
                self.device = val.get("value")
            # vendor
            elif obis_id == "129-129:199.130.3*255":
                self.vendor = val.get("value")
            # public key
            elif obis_id == "129-129:199.130.5*255":
                continue

            else:
                try:
                    self.get_metric(obis_id).labels(
                        vendor=self.vendor, device=self.device
                    ).set(val.get("value"))
                except KeyError:
                    pass
