class TagReaderWriter:
    def __init__(self):
        pass

    @staticmethod
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

    @staticmethod
    def get_uris(tag):
        if not tag.ndef:
            raise TagException("received empty ndef")
        if len(tag.ndef.records) == 0:
            raise TagException("received tag with 0 records")
        uris = []
        for index, record in enumerate(tag.ndef.records):
            if not isinstance(record, ndef.uri.UriRecord):
                raise TagException(
                    f"record {index} in tag was not {ndef.uri.UriRecord.__name__}, but was {type(record).__name__}")
            uri = record.uri
            urihandler.validate_uri(uri)
            uris.append(uri)
        return uris


class TagException(Exception):
    pass
