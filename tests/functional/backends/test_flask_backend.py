# -*- coding: utf-8 -*-
import json

from collections import OrderedDict

from flask import Flask as FlaskApplication
from hovercrafty import RouteServer

from hovercrafty.backends.wsgi import FlaskBackend

time_jsontest = RouteServer('time.jsontest.com', protocols=['http'])


TIME_DATA = OrderedDict([
    ("time", "02:44:49 AM"),
    ("milliseconds_since_epoch", 1519094689265),
    ("date", "02-20-2018"),
])

TIME_JSON = json.dumps(TIME_DATA)


@time_jsontest.route('/')
def index_synthesize_time_json(request):
    return TIME_JSON


@time_jsontest.route('/foobar', methods=['POST', 'GET'])
def foobar(request):
    return json.dumps({'foo': 'bar'})


def test_flask_register_route_side_effect():
    "FlaskBackend(server).register_routes_into(app) should be have the side-effect of registering routes in an existing Flask application instance"

    app = FlaskApplication('test_flask_register_route_side_effect')

    FlaskBackend(time_jsontest).register_routes_into(app)

    app.routes.keys().should.equal(['/', '/foobar'])

    client = app.test_client()

    client.get('/').data.should.equal(TIME_JSON)
    client.get('/foobar').data.should.equal('{"foo": "bar"}')
    client.post('/foobar').data.should.equal('{"foo": "bar"}')


def test_create_flask_application():
    "FlaskBackend(server).create_application(*args, **kw) should create a new Flask() instance with pre-mapped routes"

    app = FlaskBackend(time_jsontest).create_application('test_create_flask_application')

    app.routes.keys().should.equal(['/', '/foobar'])

    client = app.test_client()

    client.get('/').data.should.equal(TIME_JSON)
    client.get('/foobar').data.should.equal('{"foo": "bar"}')
    client.post('/foobar').data.should.equal('{"foo": "bar"}')
