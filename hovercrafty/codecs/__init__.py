# -*- coding: utf-8 -*-

class BaseCodec(object):
    def __init__(self, input_stream, output_stream):
        self.input_stream = input_stream
        self.output_stream = output_stream

    def initialize(self, *args, **kw):
        pass


class JSONStreamCodec(BaseCodec):
    pass


class UnicodeStreamCodec(BaseCodec):
    def initialize(self, encoding='utf-8'):
        self.encoding = encoding
