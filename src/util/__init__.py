import inspect
import os
import logging
import logging.handlers
import pytest
import datetime
import unittest

try:
    import simplejson as json  # pylint: disable=F0401
except ImportError:
    import json


class marker(object):

    def __init__(self):
        super(Marker, self).__init__()

    marker = getattr(pytest, 'mark')
    BVT = marker.BVT
    P0 = marker.P0
    P1 = marker.P1
    P2 = marker.P2
    DEBUG = marker.DEBUG

    SYS_TEST = marker.SYS_TEST
    INTG_TEST = marker.INTG_TEST
    FUNC_TEST = marker.FUNC_TEST
    UNIT_TEST = marker.UNIT_TEST

    xfail = marker.xfail
    skipif = marker.skipif
