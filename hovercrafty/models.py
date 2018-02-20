# -*- coding: utf-8 -*-
import re
from collections import OrderedDict
from .exceptions import RouteAlreadyDefined
from .utils import parse_destination
from .utils import parse_query_string_ordered
from .utils import split_hostname_and_path
from .utils import unique_ordered_tuple

PROTOCOL_HOSTNAME_ROUTES_SERVERS = OrderedDict()  # e.g.: "http://hostname.com"  # no trailing slash
HOSTNAME_ONLY_ROUTES_SERVERS = OrderedDict()  # e.g.: "hostname.com"
HOSTNAME_METHODS_ONLY_ROUTES_SERVERS = OrderedDict()  # e.g.: ("hostname.com", ("GET", "POST", "PUT"))
PROTOCOL_HOSTNAME_METHODS_ROUTES_SERVERS = OrderedDict()  # e.g.: ("http://hostname.com", ("HEAD", "GET")  # no trailing slash


class RouteServer(object):
    def __init__(self, destination, protocols=None, routes=None):
        info = parse_destination(destination)
        self.destination = destination
        self.protocol = info.get('protocol')
        self.schema = "{protocol}://".format(**info)
        self.hostname = info.pop('hostname')
        self.routes = OrderedDict(routes or [])
        self.protocols = unique_ordered_tuple(protocols or [] + [self.protocol])

    def clone(self, with_routes=False):
        params = {
            'protocols': self.protocols,
        }
        if with_routes:
            params['routes'] = self.routes

        return RouteServer(self.destination, **params)

    def __repr__(self):
        return r'<RouteServer({self.destination}, {self.protocols})>'.format(self=self)

    def route(self, pattern, methods=None, overwrite=False, fail=True):
        # TODO: in docstring suggest using safe if you want to log overwrites instead of raising
        methods = unique_ordered_tuple(methods or ['GET'])

        def wrapper(handler):
            self.register_route(
                pattern=pattern,
                methods=methods,
                overwrite=overwrite,
                fail=fail,
                handler=handler
            )

            return handler

        return wrapper

    def create_route_defintion(self, *args, **kw):
        return RouteDefinition(self, *args, **kw)

    def get_route_defintion(self, pattern, methods):
        key = (pattern, unique_ordered_tuple(methods))
        existing = self.routes.get(key)
        return existing

    def register_route(self, pattern, handler, methods, fail=False, overwrite=False, **route_params):
        is_safe = not fail
        existent_definition = self.get_route_defintion(pattern, methods)
        if not overwrite and existent_definition:
            if is_safe:
                self.logger.warning('replacing existing route {}'.format(existent_definition))
                return existent_definition

            raise RouteAlreadyDefined(existent_definition)

        definition = self.create_route_defintion(handler, pattern, methods, **route_params)

        # determine key for self.routes and register new route definition
        key = (pattern, unique_ordered_tuple(methods))
        self.routes[key] = definition
        # TODO: register route in all other global dictionaries
        return definition


class RouteDefinition(object):
    def __init__(self, parent, handler, pattern, methods=['GET'], protocols=['http']):
        if not isinstance(parent, RouteServer):
            msg = (
                'RouteDefinition() takes a RouteServer instance as '
                'first argument, but got {} {}.'
            )
            raise TypeError(msg.format(parent, type(parent)))
        self.handler_callable = handler
        self.server = parent
        self.hostname = parent.hostname
        self.pattern = pattern
        try:
            self.regex = re.compile(pattern)
        except re.error:
            self.regex = None

        self.routes = OrderedDict()
        self.methods = sorted(set(methods))

    def __repr__(self):
        return r'<RouteDefinition({self.parent}, {self.handler}, {self.pattern}, {self.methods, {self.protocols})>'.format(self=self)


class HttpRequest(object):
    def __init__(self, url, headers=None, query_params=None, query_string=None):
        self.url = url
        self.hostname, self.path = split_hostname_and_path(url)
        self.headers = OrderedDict(headers or [])
        self.params = OrderedDict(query_params or [])
        self.query_params = query_params
        self.query_string = query_string
        self.params.update(parse_query_string_ordered(query_params))

    def __repr__(self):
        return r'<HttpRequest({self.url}, {self.headers}, {self.query_params}, {self.query_string})>'.format(self=self)


class HttpResponse(object):
    def __init__(self, body=None, status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = OrderedDict(headers or [])

    def __repr__(self):
        return r'<HttpResponse({self.body}, {self.status}, {self.headers})>'.format(self=self)
