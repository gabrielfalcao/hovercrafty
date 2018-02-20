# -*- coding: utf-8 -*-
import re
import six
import urllib
from collections import OrderedDict


destination_pattern = re.compile(r'((?P<protocol>[^:]+)[:])?(//)?(?P<hostname>.*?])[/]*$')
DEFAULT_PROTOCOL = 'http'
DEFAULT_HOSTNAME = None


def parse_destination(string, default_protocol=DEFAULT_PROTOCOL, default_hostname=DEFAULT_HOSTNAME):
    # TODO: unit test
    found = destination_pattern.search(string)

    fresh = OrderedDict([
        ('protocol', default_protocol),
        ('hostname', default_hostname),
    ])
    if found:
        fresh.update(found.groupdict())
        return fresh

    return fresh.copy()


def clear_protocol(string):
    return parse_destination(string).get('protocol') or ''


def unique_ordered_tuple(iterable):
    if isinstance(iterable, six.string_types):
        raise TypeError('unique_ordered_tuple() does not accept a string-type, got: {}'.format(iterable))

    return tuple(iterable)


def parse_query_string_ordered(string):
    result = OrderedDict()
    return result


def split_hostname_and_path(string):
    info = urllib.urlparse(string)
    return info.hostname, info.path


def validate_type(callable_name, Type, value):
    if not isinstance(value, Type):
        module = Type.__module__
        value_type = type(value)
        msg = '{callable_name}() takes a {module} as argument, got {value} {value_type}'
        raise TypeError(msg.format(**locals()))
