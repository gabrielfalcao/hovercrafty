# -*- coding: utf-8 -*-


class Backend(object):
    def __init__(self, route_server, *args, **kw):
        self.server = route_server
        self.initialize(*args, **kw)

    def initialize(self, *args, **kw):
        pass

    def translate_request(self, request, route):
        raise NotImplementedError

    def translate_response(self, request, route):
        raise NotImplementedError

    def calculate_exact_body(self, request, response):
        raise NotImplementedError

    def calculate_exact_querystring(self, request, response):
        raise NotImplementedError
