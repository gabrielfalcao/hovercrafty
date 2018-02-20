# -*- coding: utf-8 -*-
import json

from collections import OrderedDict

from flask import Flask as FlaskApplication
from hovercrafty import RouteServer

from hovercrafty.backends.wsgi import FlaskBackend


router = RouteServer('http://time.jsontest.com')


TIME_DATA = OrderedDict([
    ("time", "02:44:49 AM"),
    ("milliseconds_since_epoch", 1519094689265),
    ("date", "02-20-2018"),
])


def get_rules_from_flask_app(app):
    return [r.rule for r in app.url_map.iter_rules()]


@router.route('/')
def index(request):
    return json.dumps(TIME_DATA)


@router.route('/foo/bar', methods=['POST', 'GET'])
def foobar(request):
    return json.dumps({'foo': 'bar'})


def test_flask_register_route_side_effect():
    "FlaskBackend(server).register_routes_into(app) should be have the side-effect of registering routes in an existing Flask application instance"

    app = FlaskApplication('test_flask_register_route_side_effect')

    FlaskBackend(router).register_routes_into(app)

    client = app.test_client()

    client.get('/').data.should.equal(json.dumps(TIME_DATA))
    client.get('/foo/bar').data.should.equal(b'{"foo": "bar"}')
    client.post('/foo/bar').data.should.equal(b'{"foo": "bar"}')

    rules = get_rules_from_flask_app(app)
    rules.should.have.length_of(3)
    rules.should.equal(['/foo/bar', '/', '/static/<path:filename>'])


def test_create_flask_application():
    "FlaskBackend(server).create_application(*args, **kw) should create a new Flask() instance with pre-mapped routes"

    app = FlaskBackend(router).create_application('test_create_flask_application')

    client = app.test_client()

    client.get('/').data.should.equal(json.dumps(TIME_DATA))
    client.get('/foo/bar').data.should.equal(b'{"foo": "bar"}')
    client.post('/foo/bar').data.should.equal(b'{"foo": "bar"}')

    rules = get_rules_from_flask_app(app)
    rules.should.have.length_of(3)
    rules.should.equal(['/foo/bar', '/', '/static/<path:filename>'])
