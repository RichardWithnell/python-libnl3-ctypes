#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ctypes import  POINTER, byref, c_void_p

from ..import  wrap_nl_err
from ..cache import NlCache
from .ct import Ct
from .import nfnl

c_nl_sock_p = c_void_p
c_nl_cache_p = c_void_p

#noinspection PyUnusedLocal
@wrap_nl_err(nfnl, c_nl_sock_p, POINTER(c_nl_cache_p))
def nfnl_ct_alloc_cache(sock, cache_p):
    """nfl_alloc_cache(struct nl_sock *, struct nl_cache **);"""


class NfNlCtCache(NlCache):
    _objclass = Ct
    _cache_name = 'netfilter/ct'

    def __init__(self, ptr=None, parent=None, sock=None):
        if ptr is not None:
            super(NfNlCtCache, self).__init__(ptr=ptr, parent=parent)
            return
        if sock is None:
            raise ValueError('sock is None')
        xxx = c_nl_cache_p()
        nfnl_ct_alloc_cache(sock, byref(xxx))
        super(NfNlCtCache, self).__init__(ptr=ptr)
        self._need_free = True
