# Copyright 2010-2014 Michael Frank <msfrank@syntaxjockey.com>
#
# This file is part of Pesky.  Pesky is BSD-licensed software;
# for copyright information see the LICENSE file.

import os
import datetime
import shlex
import re

from pesky.settings.util.args import parse_args
from pesky.settings.errors import ConversionError, ConfigureError

def str_to_stripped(s):
    return s.strip()

def str_to_flattened(s):
    return ' '.join(s.split())

def str_to_int(s):
    try:
        return int(s)
    except:
        raise ConversionError("failed to convert {0} to float".format(s))

def str_to_bool(s):
    s = s.lower()
    if s in ('true', 'yes', '1'):
        return True
    if s in ('false', 'no', '0'):
        return False
    raise ConversionError("failed to convert {0} to bool".format(s))

def str_to_float(s):
    try:
        return float(s)
    except:
        raise ConversionError("failed to convert {0} to float".format(s))

def str_to_timedelta(s):
    s = s.strip()
    try:
        m = re.match(r'([1-9]\d*)\s*(.*)', s)
        if m is None:
            raise Exception("{0} did not match regex".format(s))
        value = int(m.group(1))
        units = m.group(2).lower().strip()
        if units in ('micro', 'micros', 'microsecond', 'microseconds'):
            return datetime.timedelta(microseconds=value)
        if units in ('milli', 'millis', 'millisecond', 'milliseconds'):
            return datetime.timedelta(milliseconds=value)
        if units in ('second', 'seconds'):
            return datetime.timedelta(seconds=value)
        if units in ('minute', 'minutes'):
            return datetime.timedelta(minutes=value)
        if units in ('hour', 'hours'):
            return datetime.timedelta(hours=value)
        if units in ('day', 'days'):
            return datetime.timedelta(days=value)
        if units in ('week', 'weeks'):
            return datetime.timedelta(weeks=value)
    except Exception as e:
        raise ConversionError("failed to convert {0} to timedelta".format(s))

def str_to_size(s):
    s = s.strip()
    try:
        m = re.match(r'([1-9]\d*)\s*(.*)', s)
        if m is None:
            raise Exception("{0} did not match regex".format(s))
        value = int(m.group(1))
        units = m.group(2).lower().strip()
        if units in ('kb', 'kilo', 'kilobyte', 'kilobytes'):
            return value * 1024
        if units in ('mb', 'mega', 'megabyte', 'megabytes'):
            return value * 1024 * 1024
        if units in ('gb', 'giga', 'gigabyte', 'gigabytes'):
            return value * 1024 * 1024 * 1024
        if units in ('tb', 'tera', 'terabyte', 'terabytes'):
            return value * 1024 * 1024 * 1024 * 1024
        if units in ('pb', 'peta', 'petabyte', 'petabytes'):
            return value * 1024 * 1024 * 1024 * 1024 * 1024
    except Exception as e:
        raise ConversionError("failed to convert {0} to size in bytes".format(s))

def str_to_percentage(s):
    s = s.strip()
    try:
        m = re.match(r'(0?\.\d+|[1-9]\d*\.\d+|\d+)\s*%', s)
        if m is None:
            raise Exception("{0} did not match regex".format(s))
        return float(m.group(1)) / 100.0
    except Exception as e:
        raise ConversionError("failed to convert {0} to percentage".format(s))

def str_to_args(s, *spec, **kwargs):
    default = None
    if 'default' in kwargs:
        default = kwargs['default']
        del kwargs['default']
    try:
        return parse_args(shlex.split(s), *spec, **kwargs)
    except Exception as e:
        raise ConversionError("failed to convert {0} to args".format(s))
