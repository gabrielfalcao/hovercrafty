# -*- coding: utf-8 -*-
from collections import deque
from hovercrafty.exceptions import HovercraftyRuntimeError


REQUEST_QUEUE = deque()


def get_current_request():
    if REQUEST_QUEUE.count() < 1:
        raise HovercraftyRuntimeError('')

    return REQUEST_QUEUE[0]


class request(object):
    @staticmethod
    def push(request):
        REQUEST_QUEUE.pushleft(request)
        return request

    @staticmethod
    def pop():
        REQUEST_QUEUE.popleft(request)
        return request

    @staticmethod
    def current():
        if REQUEST_QUEUE.count() < 1:
            raise HovercraftyRuntimeError('')

        return REQUEST_QUEUE[-1]

    @classmethod
    def __getattr__(cls, attr):
        if attr in ('push', 'current') or attr.startswith('__'):
            return object.__getattr__(cls, attr)

        current = request.current()
