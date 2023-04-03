from unittest.mock import Mock, MagicMock

from sml import SmlGetListResponse  # type: ignore

from sml_exporter import __version__, SmlExporter


def test_version() -> None:
    assert __version__ == "0.1.4"


def test_kmf() -> None:
    """Test for Kaifa KFM 95002630 T11252, firmware 1.03."""
    val_list = [
        {"objName": "1-0:96.50.1*1", "value": b"KFM"},
        {"objName": "1-0:96.1.0*255", "value": "1 KFM 00 123456"},
        {
            "objName": "1-0:1.8.0*255",
            "status": 801028,  # status seems to be some kind of bit field, not sure what it's for
            "unit": "Wh",
            "value": 23.5,
        },
        {"objName": "1-0:2.8.0*255", "unit": "Wh", "value": 42.0},
        {"objName": "1-0:16.7.0*255", "unit": "W", "value": -1234},
        {"objName": "1-0:32.7.0*255", "unit": "V", "value": 240.0},
        {"objName": "1-0:52.7.0*255", "unit": "V", "value": 240.0},
        {"objName": "1-0:72.7.0*255", "unit": "V", "value": 0},
        {"objName": "1-0:31.7.0*255", "unit": "A", "value": 16.00},
        {"objName": "1-0:51.7.0*255", "unit": "A", "value": 16.00},
        {"objName": "1-0:71.7.0*255", "unit": "A", "value": 0},
        {"objName": "1-0:81.7.1*255", "unit": "°", "value": 240},
        {"objName": "1-0:81.7.2*255", "unit": "°", "value": -1},
        {"objName": "1-0:81.7.4*255", "unit": "°", "value": 180},
        {"objName": "1-0:81.7.15*255", "unit": "°", "value": 180},
        {"objName": "1-0:81.7.26*255", "unit": "°", "value": -1},
        {"objName": "1-0:14.7.0*255", "unit": "Hz", "value": 50.0},
        {"objName": "1-0:0.2.0*0", "value": b"1.03"},
        {"objName": "1-0:96.90.2*1", "value": b"~ \x05\xd2"},
    ]
    message_body = Mock(spec=SmlGetListResponse)
    message_body.get = MagicMock(return_value=val_list)
    exporter = SmlExporter()
    exporter.event(message_body)
    assert exporter.vendor == "KFM"
    assert exporter.device == "1 KFM 00 123456"
    assert exporter.metrics["1-0:1.8.0*255"].collect()[0].samples[0].value == 23.5
    assert exporter.metrics["1-0:2.8.0*255"].collect()[0].samples[0].value == 42.0
    assert len(exporter.metrics) == 15  # no unhandled OBIS ids
