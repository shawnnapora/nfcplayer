#!/home/multimedia/Desktop/reader/venv/bin/python

import ndef
import nfc
import urihandler


def get_uris(tag):
    if not tag.ndef:
        raise Exception("received empty ndef")
    if len(tag.ndef.records) == 0:
        raise Exception(f"received tag with 0 records")
    uris = []
    for index, record in enumerate(tag.ndef.records):
        if not isinstance(record, ndef.uri.UriRecord):
            raise Exception(f"record {index} in tag was not {ndef.uri.UriRecord.__name__}, but was {type(record).__name__}")
        uri = record.uri
        urihandler.validate_uri(uri)
        uris.append(uri)
    return uris

def get_on_connect(device):
    def on_connect(tag):
        try:
            uris = get_uris(tag)
            print(f"playing {repr(uris)}")
            urihandler.handle_uris(uris)
        except Exception as e:
            # invalid tag, beep now in addition to default to indicate error.
            print(e)
            device.turn_on_led_and_buzzer()
        return tag
    return on_connect


print("Opening reader")
with nfc.ContactlessFrontend('usb') as clf:
    print(f"Opened reader {clf}")
    rdwr_options = {
        'targets': ('106A',),
        'on-connect': get_on_connect(clf.device),
    }
    print("Waiting for tags")
    while True:
        clf.connect(rdwr=rdwr_options)
