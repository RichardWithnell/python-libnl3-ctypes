#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ctypes import  c_uint64, c_int, c_void_p
from ...import wrap_int, wrap_custom
from ..nlobject import NlObject
from .import nfnl

c_nfnl_ct_p = c_void_p

#noinspection PyUnusedLocal
@wrap_int(nfnl, c_nfnl_ct_p, c_int)
def nfnl_ct_test_packets(ct, direction):
    pass

#noinspection PyUnusedLocal
@wrap_int(nfnl, c_nfnl_ct_p, c_int)
def nfnl_ct_test_bytes(ct, direction):
    pass

#noinspection PyUnusedLocal
@wrap_custom(nfnl, c_uint64, c_nfnl_ct_p, c_int)
def nfnl_ct_get_packets(ct, direction):
    pass

#noinspection PyUnusedLocal
@wrap_custom(nfnl, c_uint64, c_nfnl_ct_p, c_int)
def nfnl_ct_get_bytes(ct, direction):
    pass


class Ct(NlObject):
    test_packets = lambda self, direction: bool(nfnl_ct_test_packets(self, direction))
    test_bytes = lambda self, direction: bool(nfnl_ct_test_bytes(self, direction))

    get_packets = lambda self, direction: nfnl_ct_get_packets(self, direction)
    get_bytes = lambda self, direction: nfnl_ct_get_bytes(self, direction)
