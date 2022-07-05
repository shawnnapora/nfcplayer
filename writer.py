#!./venv/bin/python

import nfc
import ndef
import sys
import urihandler


def write_tag(tag, new_records):
    if tag.ndef is None:
        print("This is not an NDEF Tag.")
        return

    if not tag.ndef.is_writeable:
        print("This Tag is not writeable.")
        return

    message_length = sum([len(r) for r in ndef.message.message_encoder(new_records)])
    if message_length > tag.ndef.capacity:
        print("The new tag data exceeds the Tag's capacity.")
        return

    tag.ndef.records = new_records


records = []
for arg in sys.argv[1:]:
    urihandler.validate_uri(arg)
    records.append(ndef.UriRecord(arg))

if len(records) == 0:
    raise Exception("need at least one argument to write")

with nfc.ContactlessFrontend('usb') as clf:
    rdwr_options = {
        'targets': ('106A',),
        'on-connect': lambda tag: write_tag(tag, records),
    }
    clf.connect(rdwr=rdwr_options)
    print(f"loaded tag with records: {repr(records)}")
