#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ctypes import c_bool, c_uint64, c_int, c_void_p
from .. import wrap
from . import nfnl
from ..nlobject import NlObject

c_nfnl_ct_p = c_void_p

class Ct(NlObject):
    # returnc c_int in original..
    @wrap(nfnl, None, c_bool, c_nfnl_ct_p, c_int)
    def nfnl_ct_test_packets(): pass

    # returnc c_int in original..
    @wrap(nfnl, None, c_bool, c_nfnl_ct_p, c_int)
    def nfnl_ct_test_bytes(): pass


    # returnc c_int in original..
    @wrap(nfnl, None, c_uint64, c_nfnl_ct_p, c_int)
    def nfnl_ct_get_packets(): pass

    # returnc c_int in original..
    @wrap(nfnl, None, c_uint64, c_nfnl_ct_p, c_int)
    def nfnl_ct_get_bytes(): pass
