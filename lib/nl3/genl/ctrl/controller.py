#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ....ctypes.libnl3_genl import *
from ...cache import NlCache
from ..socket import Socket
from .genl_family import Family

#TODO: _obj_class = Family ?
class CtrlCache(NlCache):
    _cache_name = 'genl/family'

    def __init__(self, ptr=None, parent=None, sock=None):
        if ptr is not None:
            super(CtrlCache, self).__init__(ptr, parent)
            return
        if sock is None:
            sock = Socket()
            sock.connect()
        else:
            if sock.get_fd() == -1:
                raise RuntimeError('cache expect connected socket')

        xxx = genl_ctrl_alloc_cache(sock)
        super(CtrlCache, self).__init__(ptr=xxx)
        self._sock = sock # prevent from garbage collecting
        self._need_free = True

    def search_by_name(self, name):
        ptr = genl_ctrl_search_by_name(self, name)
        return Family(ptr=ptr, parent=self)

    def search(self, id):
        ptr = genl_ctrl_search(self, id)
        return Family(ptr=ptr, parent=self)
