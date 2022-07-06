#!/usr/bin/env python

import ndef
import nfc
import urihandlers

from urllib.parse import urlparse
from urihandlers import AlbumHandler


handlers = {
    AlbumHandler.Scheme: AlbumHandler("/home/multimedia/SeaDrive/Shared with groups/Media/Music")
}


def handle_uris(uris):
    previous = None
    parsed_uris = []
    for uri in uris:
        parsed = urlparse(uri)
        if previous is not None and previous.scheme != parsed.scheme:
            raise Exception(f"multiple schemes may not be used (found {parsed.scheme} and {previous.scheme}")
        if parsed.scheme not in handlers:
            raise Exception("provided scheme unsupported")
        previous = parsed
        parsed_uris.append(parsed)
    handlers[parsed.scheme].handle_uris(parsed_uris)


def validate_uri(uri):
    parsed = urlparse(uri)
    if parsed.scheme not in handlers:
        raise Exception(f"scheme {parsed.scheme} not in handlers: {repr(handlers.keys())}")
    handlers[parsed.scheme].validate_uri(parsed)


def get_uris(tag):
    if not tag.ndef:
        raise Exception("received empty ndef")
    if len(tag.ndef.records) == 0:
        raise Exception("received tag with 0 records")
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
