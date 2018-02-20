# -*- coding: utf-8 -*-
from flask import Flask
from hovercrafty.http import request
from hovercrafty.models import HttpRequest
from hovercrafty.utils import validate_type

from hovercrafty.backends.base import Backend


class WSGIBackend(Backend):
    def __init__(self, route_server):
        self.server = route_server


class FlaskBackend(WSGIBackend):

    def translate_request(self, request, route):
        """
        :param request: a :py:class:`hovercrafty.models.HttpRequest` instance
        """
        validate_type('FlaskBackend.translate_request', HttpRequest, request)

        response = self.process_request(request, route)
        result = {
	    "path": {
		"exactMatch": route.pattern,
	    },
	    "method": {
		"exactMatch": request.method,
	    },
	    "destination": {
		"exactMatch": route.server.hostname,
	    },
	    "scheme": {
		"exactMatch": "http",
	    },
	    "query": {
		"exactMatch": route.calculate_exact_querystring(request, response),
	    },
	    "body": {
		"exactMatch": route.calculate_exact_body(request, response),
	    }
	}
        return result

    def calculate_exact_body(self, request, response):
        return response.as_string()

    def calculate_exact_querystring(self, request, response):
        return response.get_querystring()

    def register_routes_into(self, flask_app):
        for route in self.server.routes.values():
            flask_app.add_url_rule(
                route.pattern,
                route.endpoint,
                view_func=lambda *args, **kw: route.handler(request, *args, **kw)
            )
        return flask_app

    def create_application(self, *args, **kw):
        app = Flask(*args, **kw)
        return self.register_routes_into(app)
