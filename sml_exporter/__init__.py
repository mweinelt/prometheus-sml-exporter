import logging
from threading import Timer
from typing import Dict, Optional

from prometheus_client import Gauge
from sml import SmlGetListResponse, SmlSequence  # type: ignore

logger = logging.getLogger(__name__)

# https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm
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
    "1-0:32.7.0*255": (Gauge, "smartmeter_spannung_l1_v", "Spannung L1"),
    "1-0:52.7.0*255": (Gauge, "smartmeter_spannung_l2_v", "Spannung L2"),
    "1-0:72.7.0*255": (Gauge, "smartmeter_spannung_l3_v", "Spannung L3"),
    "1-0:31.7.0*255": (Gauge, "smartmeter_strom_l1_a", "Strom L1"),
    "1-0:51.7.0*255": (Gauge, "smartmeter_strom_l2_a", "Strom L2"),
    "1-0:71.7.0*255": (Gauge, "smartmeter_strom_l3_a", "Strom L3"),
    "1-0:81.7.1*255": (
        Gauge,
        "smartmeter_phasenwinkel_ul2_ul1_deg",
        "Phasenwinkel UL2: UL1",
    ),
    "1-0:81.7.2*255": (
        Gauge,
        "smartmeter_phasenwinkel_ul3_ul1_deg",
        "Phasenwinkel UL3 : UL1",
    ),
    "1-0:81.7.4*255": (
        Gauge,
        "smartmeter_phasenwinkel_il1_ul1_deg",
        "Phasenwinkel IL1 : UL1",
    ),
    "1-0:81.7.15*255": (
        Gauge,
        "smartmeter_phasenwinkel_il2_ul2_deg",
        "Phasenwinkel IL2 : UL2",
    ),
    "1-0:81.7.26*255": (
        Gauge,
        "smartmeter_phasenwinkel_il3_ul3_deg",
        "Phasenwinkel IL3 : UL3",
    ),
    "1-0:14.7.0*255": (Gauge, "smartmeter_netzfrequenz_hz", "Netzfrequenz"),
}

WATCHDOG_TIMEOUT_SECS = 10


class SmlExporter:
    def __init__(self) -> None:
        self.device: Optional[str] = None
        self.vendor: Optional[str] = None
        self.metrics: Dict[str, Gauge] = {}
        self.init_watchdog()

    def get_metric(self, obis_id: str) -> Gauge:
        # skip until we have seen vendor and device identifier, so we can populate the according labels
        if not self.device or not self.vendor:
            raise ValueError

        if obis_id in self.metrics:
            return self.metrics[obis_id]

        try:
            _type, name, desc = OBIS[obis_id]
        except KeyError:
            raise UnhandledObisId

        metric = _type(name, f"{desc} ({obis_id})", ["vendor", "device"])
        self.metrics[obis_id] = metric

        return metric

    def event(self, message_body: SmlSequence) -> None:
        logger.debug(f"message_body: {message_body!r}")
        assert isinstance(message_body, SmlGetListResponse)
        for val in message_body.get("valList", []):
            obis_id = val.get("objName")

            # device id
            if obis_id in [
                "1-0:0.0.9*255",
                "1-0:96.1.0*255",  # KFM
            ]:
                device = val.get("value")
                if self.device != device:
                    logger.info(f"device: {device}")
                self.device = device
            # vendor
            elif obis_id in [
                "129-129:199.130.3*255",
                "1-0:96.50.1*1",  # KFM
            ]:
                vendor = val.get("value")
                try:
                    vendor = vendor.decode()
                except (UnicodeDecodeError, AttributeError):
                    pass
                if self.vendor != vendor:
                    logger.info(f"vendor: {vendor}")
                self.vendor = vendor
            # public key
            elif obis_id == "129-129:199.130.5*255":
                continue
            # firmware version
            elif obis_id == "1-0:0.2.0*0":
                continue
            # CRC of configured parameters:
            elif obis_id == "1-0:96.90.2*1":
                continue

            else:
                try:
                    self.get_metric(obis_id).labels(
                        vendor=self.vendor, device=self.device
                    ).set(val.get("value"))
                except ValueError:
                    pass
                except UnhandledObisId:
                    logger.warning(
                        f"Unhandled OBIS ID: {obis_id} = {val.get('value')} {val.get('unit','')}"
                    )

        for val in message_body.get("valList", []):
            logger.debug(
                f'{val.get("objName"):<15} {val.get("value")!r:>17} {val.get("unit", "")}'
            )
        if not self.device or not self.vendor:
            logger.debug(
                "Vendor or device identifiers not initialized, event was ignored."
            )
        self.reset_watchdog()

    def clear_metrics(self):
        logger.warning("Timeout on receiving serial data, clearing metrics.")
        for metric in self.metrics.values():
            metric.clear()

    def init_watchdog(
        self,
    ):
        """Start a timer that clears data from metrics if not cancelled in time."""
        logger.debug(
            f"Setting watchdog for getting new data with a {WATCHDOG_TIMEOUT_SECS} timeout."
        )
        timer = Timer(WATCHDOG_TIMEOUT_SECS, self.clear_metrics)
        timer.start()
        self.watchdog = timer

    def reset_watchdog(self):
        self.watchdog.cancel()
        self.init_watchdog()


class UnhandledObisId(Exception):
    pass
