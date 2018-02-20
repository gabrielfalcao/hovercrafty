# -*- coding: utf-8 -*-

from collections import OrderedDict
from copy import deepcopy
from flask import Flask
from hovercrafty.http import request
# from hovercrafty.models import HttpRequest
from hovercrafty.models import RouteServer
from hovercrafty.utils import validate_type

from hovercrafty.backends.base import Backend


class WSGIBackend(Backend):
    def __init__(self, route_server):
        validate_type(self.__class__.__name__, RouteServer, route_server)
        self.server = route_server


class FlaskBackend(WSGIBackend):
    def register_routes_into(self, flask_app, **rule_params):
        for (rule, methods), route in self.server.routes.items():
            params = OrderedDict(deepcopy(rule_params))
            handler = deepcopy(route.handler)
            view_func = lambda *args, **kw: handler(request, *args, **kw)
            params['rule'] = route.pattern
            params['endpoint'] = route.endpoint
            params['methods'] = route.methods
            params['view_func'] = view_func
            params['strict_slashes'] = True

            flask_app.add_url_rule(**params)

        return flask_app

    def create_application(self, *args, **kw):
        app = Flask(*args, **kw)
        return self.register_routes_into(app)
