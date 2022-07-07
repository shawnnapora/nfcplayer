#!/usr/bin/env python

import ndef
import nfc
import signal
import sys

from urihandler import UriHandler, HandlerException
from tagreaderwriter import TagReaderWriter, TagException

urihandler = UriHandler("config.yaml")
tagreaderwriter = TagReaderWriter()

print("Opening reader")
with nfc.ContactlessFrontend('usb') as clf:
    print(f"Opened reader {clf}")

    def on_connect(tag):
        try:
            uris = tagreaderwriter.get_uris(tag)
            print(f"playing {repr(uris)}")
            urihandler.handle_uris(uris)
        except (TagException, HandlerException) as e:
            # invalid tag, beep now in addition to default to indicate error.
            print(e)
            clf.device.turn_on_led_and_buzzer()
        return tag

    rdwr_options = {
        'targets': ('106A',),
        'on-connect': on_connect,
    }

    # dumb/simple way to handle control-c, otherwise clf.connect doesn't respect control-c
    signal.signal(signal.SIGINT, lambda _, __: sys.exit(0))

    print("Waiting for tags")
    while True:
        clf.connect(rdwr=rdwr_options)
