#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ctypes import c_int, POINTER, byref
from ... import swrap
from .. import errcode_check
from . import nfnl

from ..socket import c_nl_sock_p
from ..cache import NlCache, c_nl_cache_p
from .ct import Ct

@swrap(nfnl, errcode_check, c_int, c_nl_sock_p, POINTER(c_nl_cache_p))
def nfnl_ct_alloc_cache():
    """nfl_alloc_cache(struct nl_sock *, struct nl_cache **);"""

class NfNlCtCache(NlCache):
    _objclass = Ct

    def __init__(self, sock):
        xxx = c_nl_cache_p()
        self._alloc_ptr = lambda : xxx if nfnl_ct_alloc_cache(sock, byref(xxx)) else xxx
        super(NfNlCtCache, self).__init__()
