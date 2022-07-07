import inspect
import urihandlers
import yaml
from urllib.parse import urlparse


class UriHandler:
    def __init__(self, config_file):
        self.handlers = {}
        handler_config = self.read_config(config_file)
        for _, cls in inspect.getmembers(urihandlers, inspect.isclass):
            if cls.__name__ not in handler_config:
                continue
            handler = cls(**handler_config[cls.__name__])
            self.handlers[handler.Scheme] = handler

    @staticmethod
    def read_config(config_file):
        with open(config_file) as config_stream:
            config = yaml.safe_load(config_stream)
            if "urihandlers" in config:
                return config["urihandlers"]
            return {}

    def handle_uris(self, uris):
        previous = None
        parsed_uris = []
        for uri in uris:
            self.validate_uri(uri)
            parsed = urlparse(uri)
            if previous is not None and previous.scheme != parsed.scheme:
                raise HandlerException(f"multiple schemes may not be used (found {parsed.scheme} and {previous.scheme}")
            previous = parsed
            parsed_uris.append(parsed)
        self.handlers[parsed.scheme].handle_uris(parsed_uris)

    def validate_uri(self, uri):
        parsed = urlparse(uri)
        if parsed.scheme not in handlers:
            raise HandlerException(f"scheme {parsed.scheme} not in handlers: {repr(handlers.keys())}")
        self.handlers[parsed.scheme].validate_uri(parsed)


class HandlerException(Exception):
    pass
