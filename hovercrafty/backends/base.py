# -*- coding: utf-8 -*-
from hovercrafty.models import HttpRequest


class Backend(object):
    def translate_request(self, request, route):
        raise NotImplementedError

    def translate_response(self, request, route):
        raise NotImplementedError

    def calculate_exact_body(self, request, response):
        raise NotImplementedError

    def calculate_exact_querystring(self, request, response):
        raise NotImplementedError
