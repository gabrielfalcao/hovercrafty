# -*- coding: utf-8 -*-
import re
from collections import OrderedDict
from .exceptions import RouteAlreadyDefined
from utils import parse_destination
from utils import unique_ordered_tuple

PROTOCOL_HOSTNAME_ROUTES_SERVERS = OrderedDict()  # e.g.: "http://hostname.com"  # no trailing slash
HOSTNAME_ONLY_ROUTES_SERVERS = OrderedDict()  # e.g.: "hostname.com"
HOSTNAME_METHODS_ONLY_ROUTES_SERVERS = OrderedDict()  # e.g.: ("hostname.com", ("GET", "POST", "PUT"))
PROTOCOL_HOSTNAME_METHODS_ROUTES_SERVERS = OrderedDict()  # e.g.: ("http://hostname.com", ("HEAD", "GET")  # no trailing slash


class RouteServer(object):
    def __init__(self, destination):
        info = parse_destination(destination)
        self.destination = destination
        self.protocol = info.pop('protocol')
        self.schema = "{protocol}://".format(**info)
        self.hostname = info.pop('hostname')
        self.routes = OrderedDict()

    def route(self, pattern, methods, overwrite=False, fail=True):
        # TODO: in docstring suggest using safe if you want to log overwrites instead of raising
        methods = unique_ordered_tuple(methods)

        route = self.get_route_defintion(pattern, methods)

        # determine key for self.routes
        key = (pattern, unique_ordered_tuple(methods))
        self.register_route_by_key(
            key=key,
            overwrite=overwrite,
            fail=fail,
            pattern=pattern,
            methods=methods,
        )
        return route

    def create_route_defintion(self, *args, **kw):
        return RouteDefinition(self, *args, **kw)

    def get_route_defintion(self, pattern, methods):
        key = (pattern, unique_ordered_tuple(methods))
        existing = self.routes.get(key)
        return existing

    def register_route_by_key(self, key, **route_params):
        force_overwrite = route_params.pop('overwrite', False)
        existent_definition = self.get_route_defintion(**route_params)
        if not force_overwrite and existent_definition:
            raise RouteAlreadyDefined(existent_definition)

        self.routes[key] = self.create_route_defintion(**route_params)


class RouteDefinition(object):
    def __init__(self, parent, pattern, methods=['GET'], protocols=['http']):
        if not isinstance(parent, RouteServer):
            msg = (
                'RouteDefinition() takes a RouteServer instance as '
                'first argument, but got {} {}.'
            )
            raise TypeError(msg.format(parent, type(parent)))
        self.server = parent
        self.hostname = parent.hostname
        self.pattern = pattern
        try:
            self.regex = re.compile(pattern)
        except re.error:
            self.regex = None

        self.routes = OrderedDict()
        self.methods = sorted(set(methods))
