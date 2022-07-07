#!/usr/bin/env python

import nfc
import ndef
import sys
from urihandler import UriHandler
from tagreaderwriter import TagReaderWriter


urihandler = UriHandler("config.yaml")
tagreaderwriter = TagReaderWriter()

records = []
for arg in sys.argv[1:]:
    urihandler.validate_uri(arg)
    records.append(ndef.UriRecord(arg))

if len(records) == 0:
    raise Exception("need at least one argument to write")

with nfc.ContactlessFrontend('usb') as clf:
    rdwr_options = {
        'targets': ('106A',),
        'on-connect': lambda tag: tagreaderwriter.write_tag(tag, records),
    }
    clf.connect(rdwr=rdwr_options)
    print(f"loaded tag with records: {repr(records)}")
