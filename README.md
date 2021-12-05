# sml-exporter

[Prometheus](https://prometheus.io/) Exporter for smart meters that communicate using the [SML language](https://de.wikipedia.org/wiki/Smart_Message_Language), which is widely available through read-only interfaces on smart power meters in Germany.

Built on top of [pysml](https://github.com/mtdcr/pysml), which does most of the heavy lifting, by parsing the message stream into python objects.

## Install

The [package](https://pypi.org/project/sml-exporter/) can be installed from [PyPi](https://pypi.org). It provides an executable that should be installed automatically into your environment.

```
$ python3 -m pip install sml-exporter
```

Update an existing installation using

```
$ python3 -m pip install -U sml-exporter
```

## Usage

The only two options available configure the serial interface where your USB to D0 (or similiar) adapter is connected at. Setting an explicit port number is useful when you have multiple power meters.

```
❯ sml-exporter --help
Usage: sml-exporter [OPTIONS] TTY

Options:
  -p, --http-port INTEGER RANGE  HTTP Port for the Prometheus Exporter
                                 [default: 9761]

  --help                         Show this message and exit.
```

Make sure to use stable device symlinks provided by `/dev/serial/by-id/`, so you don't mixup different serial devices.

```
# ls /dev/serial/by-id/
usb-FTDI_FT232R_USB_UART_XXXXXXXX-if00-port0
usb-FTDI_FT232R_USB_UART_YYYYYYYY-if00-port0
```

## Metrics

Metrics are identified by their [OBIS](https://de.wikipedia.org/wiki/OBIS-Kennzahlen) numbering and transformed into a the following metrics:

```
# HELP smartmeter_wirkarbeit_verbrauch_total_wh Summe Wirkarbeit Verbrauch über alle Tarife (1-0:1.8.0*255)
# TYPE smartmeter_wirkarbeit_verbrauch_total_wh gauge
smartmeter_wirkarbeit_verbrauch_total_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 6.8437382e+06
# HELP smartmeter_wirkarbeit_lieferung_total_wh Summe Wirkarbeit Lieferung über alle Tarife (1-0:2.8.0*255)
# TYPE smartmeter_wirkarbeit_lieferung_total_wh gauge
smartmeter_wirkarbeit_lieferung_total_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 5.8312058e+06
# HELP smartmeter_wirkarbeit_verbrauch_tarif1_wh Summe Wirkarbeit Verbrauch im Tarif 1 (1-0:1.8.1*255)
# TYPE smartmeter_wirkarbeit_verbrauch_tarif1_wh gauge
smartmeter_wirkarbeit_verbrauch_tarif1_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 6.8437382e+06
# HELP smartmeter_wirkarbeit_lieferung_tarif1_wh Summe Wirkarbeit Lieferung im Tarif 1 (1-0:2.8.1*255)
# TYPE smartmeter_wirkarbeit_lieferung_tarif1_wh gauge
smartmeter_wirkarbeit_lieferung_tarif1_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 5.8312058e+06
# HELP smartmeter_wirkarbeit_verbrauch_tarif2_wh Summe Wirkarbeit Verbrauch im Tarif 2 (1-0:1.8.2*255)
# TYPE smartmeter_wirkarbeit_verbrauch_tarif2_wh gauge
smartmeter_wirkarbeit_verbrauch_tarif2_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 0.0
# HELP smartmeter_wirkarbeit_lieferung_tarif2_wh Summe Wirkarbeit Lieferung im Tarif 2 (1-0:2.8.2*255)
# TYPE smartmeter_wirkarbeit_lieferung_tarif2_wh gauge
smartmeter_wirkarbeit_lieferung_tarif2_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 0.0
# HELP smartmeter_wirkleistung_w Momentane Wirkleistung (1-0:16.7.0*255)
# TYPE smartmeter_wirkleistung_w gauge
smartmeter_wirkleistung_w{device="1 EMH00 XXXXXXXX",vendor="EMH"} 892.4
# HELP smartmeter_wirkarbeit_verbrauch_total_wh Summe Wirkarbeit Verbrauch über alle Tarife (1-0:1.8.0*255)
# TYPE smartmeter_wirkarbeit_verbrauch_total_wh gauge
smartmeter_wirkarbeit_verbrauch_total_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 6.8437382e+06
# HELP smartmeter_wirkarbeit_lieferung_total_wh Summe Wirkarbeit Lieferung über alle Tarife (1-0:2.8.0*255)
# TYPE smartmeter_wirkarbeit_lieferung_total_wh gauge
smartmeter_wirkarbeit_lieferung_total_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 5.8312058e+06
# HELP smartmeter_wirkarbeit_verbrauch_tarif1_wh Summe Wirkarbeit Verbrauch im Tarif 1 (1-0:1.8.1*255)
# TYPE smartmeter_wirkarbeit_verbrauch_tarif1_wh gauge
smartmeter_wirkarbeit_verbrauch_tarif1_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 6.8437382e+06
# HELP smartmeter_wirkarbeit_lieferung_tarif1_wh Summe Wirkarbeit Lieferung im Tarif 1 (1-0:2.8.1*255)
# TYPE smartmeter_wirkarbeit_lieferung_tarif1_wh gauge
smartmeter_wirkarbeit_lieferung_tarif1_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 5.8312058e+06
# HELP smartmeter_wirkarbeit_verbrauch_tarif2_wh Summe Wirkarbeit Verbrauch im Tarif 2 (1-0:1.8.2*255)
# TYPE smartmeter_wirkarbeit_verbrauch_tarif2_wh gauge
smartmeter_wirkarbeit_verbrauch_tarif2_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 0.0
# HELP smartmeter_wirkarbeit_lieferung_tarif2_wh Summe Wirkarbeit Lieferung im Tarif 2 (1-0:2.8.2*255)
# TYPE smartmeter_wirkarbeit_lieferung_tarif2_wh gauge
smartmeter_wirkarbeit_lieferung_tarif2_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 0.0
# HELP smartmeter_wirkleistung_w Momentane Wirkleistung (1-0:16.7.0*255)
# TYPE smartmeter_wirkleistung_w gauge
smartmeter_wirkleistung_w{device="1 EMH00 XXXXXXXX",vendor="EMH"} 892.4# HELP smartmeter_wirkarbeit_verbrauch_total_wh Summe Wirkarbeit Verbrauch über alle Tarife (1-0:1.8.0*255)
# TYPE smartmeter_wirkarbeit_verbrauch_total_wh gauge
smartmeter_wirkarbeit_verbrauch_total_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 6.8437382e+06
# HELP smartmeter_wirkarbeit_lieferung_total_wh Summe Wirkarbeit Lieferung über alle Tarife (1-0:2.8.0*255)
# TYPE smartmeter_wirkarbeit_lieferung_total_wh gauge
smartmeter_wirkarbeit_lieferung_total_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 5.8312058e+06
# HELP smartmeter_wirkarbeit_verbrauch_tarif1_wh Summe Wirkarbeit Verbrauch im Tarif 1 (1-0:1.8.1*255)
# TYPE smartmeter_wirkarbeit_verbrauch_tarif1_wh gauge
smartmeter_wirkarbeit_verbrauch_tarif1_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 6.8437382e+06
# HELP smartmeter_wirkarbeit_lieferung_tarif1_wh Summe Wirkarbeit Lieferung im Tarif 1 (1-0:2.8.1*255)
# TYPE smartmeter_wirkarbeit_lieferung_tarif1_wh gauge
smartmeter_wirkarbeit_lieferung_tarif1_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 5.8312058e+06
# HELP smartmeter_wirkarbeit_verbrauch_tarif2_wh Summe Wirkarbeit Verbrauch im Tarif 2 (1-0:1.8.2*255)
# TYPE smartmeter_wirkarbeit_verbrauch_tarif2_wh gauge
smartmeter_wirkarbeit_verbrauch_tarif2_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 0.0
# HELP smartmeter_wirkarbeit_lieferung_tarif2_wh Summe Wirkarbeit Lieferung im Tarif 2 (1-0:2.8.2*255)
# TYPE smartmeter_wirkarbeit_lieferung_tarif2_wh gauge
smartmeter_wirkarbeit_lieferung_tarif2_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 0.0
# HELP smartmeter_wirkleistung_w Momentane Wirkleistung (1-0:16.7.0*255)
# TYPE smartmeter_wirkleistung_w gauge
smartmeter_wirkleistung_w{device="1 EMH00 XXXXXXXX",vendor="EMH"} 892.4# HELP smartmeter_wirkarbeit_verbrauch_total_wh Summe Wirkarbeit Verbrauch über alle Tarife (1-0:1.8.0*255)
# TYPE smartmeter_wirkarbeit_verbrauch_total_wh gauge
smartmeter_wirkarbeit_verbrauch_total_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 6.8437382e+06
# HELP smartmeter_wirkarbeit_lieferung_total_wh Summe Wirkarbeit Lieferung über alle Tarife (1-0:2.8.0*255)
# TYPE smartmeter_wirkarbeit_lieferung_total_wh gauge
smartmeter_wirkarbeit_lieferung_total_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 5.8312058e+06
# HELP smartmeter_wirkarbeit_verbrauch_tarif1_wh Summe Wirkarbeit Verbrauch im Tarif 1 (1-0:1.8.1*255)
# TYPE smartmeter_wirkarbeit_verbrauch_tarif1_wh gauge
smartmeter_wirkarbeit_verbrauch_tarif1_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 6.8437382e+06
# HELP smartmeter_wirkarbeit_lieferung_tarif1_wh Summe Wirkarbeit Lieferung im Tarif 1 (1-0:2.8.1*255)
# TYPE smartmeter_wirkarbeit_lieferung_tarif1_wh gauge
smartmeter_wirkarbeit_lieferung_tarif1_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 5.8312058e+06
# HELP smartmeter_wirkarbeit_verbrauch_tarif2_wh Summe Wirkarbeit Verbrauch im Tarif 2 (1-0:1.8.2*255)
# TYPE smartmeter_wirkarbeit_verbrauch_tarif2_wh gauge
smartmeter_wirkarbeit_verbrauch_tarif2_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 0.0
# HELP smartmeter_wirkarbeit_lieferung_tarif2_wh Summe Wirkarbeit Lieferung im Tarif 2 (1-0:2.8.2*255)
# TYPE smartmeter_wirkarbeit_lieferung_tarif2_wh gauge
smartmeter_wirkarbeit_lieferung_tarif2_wh{device="1 EMH00 XXXXXXXX",vendor="EMH"} 0.0
# HELP smartmeter_wirkleistung_w Momentane Wirkleistung (1-0:16.7.0*255)
# TYPE smartmeter_wirkleistung_w gauge
smartmeter_wirkleistung_w{device="1 EMH00 XXXXXXXX",vendor="EMH"} 892.4
```

## Caveats

The exporter caches new values as they arrive, until they are overwritten by newer ones. This design was chosen as the arrival of data usually does not match up with any particular polling interval.
In an ideal world we would migrate this exporter to reuse [pushgateway](https://github.com/prometheus/pushgateway). This did not happen because I don't have any experience using it.

## License

This software is provided under the [MIT license](LICENSE) and uses
  - [pysml](https://pypi.org/project/pysml/) MIT
  - [click](https://pypi.org/project/click/) BSD3
  - [prometheus-client](https://pypi.org/project/prometheus-client/) ASL20
