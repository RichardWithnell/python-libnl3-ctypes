#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ...ctypes.libnl3_nf import *
from ..cache import NlCache
from .ct import Ct


class NfNlCtCache(NlCache):
    _objclass = Ct
    _cache_name = 'netfilter/ct'

    def __init__(self, ptr=None, parent=None, sock=None):
        if ptr is not None:
            super(NfNlCtCache, self).__init__(ptr=ptr, parent=parent)
            return
        if sock is None:
            raise ValueError('sock is None')

        xxx = nfnl_ct_alloc_cache(sock)
        super(NfNlCtCache, self).__init__(ptr=xxx)
        self._need_free = True
