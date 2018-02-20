# -*- coding: utf-8 -*-
from hovercrafty.models import HttpRequest


class Backend(object):
    def translate_request(self, request, route):
        """
        :param request: a :py:class:`hovercrafty.models.HttpRequest` instance
        """

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
		"exactMatch": "http"
	    },
	    "query": {
		"exactMatch": route.calculate_exact_querystring(request, response)
	    },
	    "body": {
		"exactMatch": route.calculate_exact_body(request, response)
	    }
	}
        return result

    def calculate_exact_body(self, request, response):
        return response.as_string()

    def calculate_exact_querystring(self, request, response):
        return response.get_querystring()
