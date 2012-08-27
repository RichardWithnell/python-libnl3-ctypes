#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ctypes import c_int, POINTER, byref
from ... import swrap
from .. import errcode_check
from . import nfnl

from ..socket import c_nl_sock_p, Socket
from ..cache import NlCache, c_nl_cache_p, cache_name2class
from .ct import Ct

@swrap(nfnl, errcode_check, c_int, c_nl_sock_p, POINTER(c_nl_cache_p))
def nfnl_ct_alloc_cache():
    """nfl_alloc_cache(struct nl_sock *, struct nl_cache **);"""

cache_name = 'netfilter/ct'

class NfNlCtCache(NlCache):
    _objclass = Ct

    def __init__(self, arg):
        if isinstance(arg, Socket):
            sock = arg
            xxx = c_nl_cache_p()
            self._alloc_ptr = lambda : xxx if nfnl_ct_alloc_cache(sock, byref(xxx)) else xxx
            super(NfNlCtCache, self).__init__()
            return
        if isinstance(arg, c_nl_cache_p):
            super(NfNlCtCache, self).__init__(arg)
            return
        raise ValueError('Unknown argument passed to constructor: %r', arg)

cache_name2class[cache_name] = NfNlCtCache
