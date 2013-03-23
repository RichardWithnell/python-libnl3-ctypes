#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ...ctypes.libnl3_nf import *
from ..nlobject import NlObject


class Ct(NlObject):
    test_packets = lambda self, direction: bool(nfnl_ct_test_packets(self, direction))
    test_bytes = lambda self, direction: bool(nfnl_ct_test_bytes(self, direction))

    get_packets = lambda self, direction: nfnl_ct_get_packets(self, direction)
    get_bytes = lambda self, direction: nfnl_ct_get_bytes(self, direction)
