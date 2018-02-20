# -*- coding: utf-8 -*-
import io
import json
import sys

from collections import OrderedDict
from hovercrafty import RouteServer

from hovercrafty.backends.hoverfly import HoverflyBackend
from hovercrafty.codecs import JSONStreamCodec
from hovercrafty.codecs import UnicodeStreamCodec

time_jsontest = RouteServer('time.jsontest.com', protocols=['http'])

time_jsontest_synthesize = time_jsontest.clone(with_routes=True)


@time_jsontest.route('/')
def index_synthesize_time_json(request):
    data = OrderedDict([
        ("time", "02:44:49 AM"),
        ("milliseconds_since_epoch", 1519094689265),
        ("date", "02-20-2018"),
    ])
    return json.dumps(data)


def test_hoverfly_synthesize():
    "HoverflyBackend(server).middleware() should source from a file-like object"
    input_stream = io.StringIO()
    output_stream = io.StringIO()

    input_stream.write(json.dumps(
        OrderedDict([
            ("time", "02:44:49 AM"),
            ("milliseconds_since_epoch", 1519094689265),
            ("date", "02-20-2018"),
        ])
    ))
    input_stream.seek(0)

    HoverflyBackend(time_jsontest_synthesize).middleware(
        input_stream=input_stream,
        output_stream=output_stream,
        codecs=[JSONStreamCodec, UnicodeStreamCodec]
    )

    json_result = output_stream.getvalue()

    json_result.should.match(r'time.*02:44:49 AM')
    json_result.should.match(r'milliseconds_since_epoch.*1519094689265')
    json_result.should.match(r'date.*02-20.2018')
