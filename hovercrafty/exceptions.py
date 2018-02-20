# -*- coding: utf-8 -*-


class RouteAlreadyDefined(Exception):
    def __init__(self, route_definition):
        msg = '{route.regex} already defined for {route.methods} on {route.hostname}'
        return super(RouteAlreadyDefined, self).__init__(msg.format(definition=route_definition))
