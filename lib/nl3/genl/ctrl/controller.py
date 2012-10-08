#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ctypes import c_int, c_char_p, POINTER, byref, c_void_p
from ....import wrap_ptr
from ...import wrap_nl_err
from ...cache import NlCache
from ..socket import Socket
from .import genl
from .genl_family import Family

c_nl_sock_p = c_void_p
c_nl_cache_p = c_void_p


#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p, POINTER(c_nl_cache_p))
def genl_ctrl_alloc_cache(sock, presult):
    """ int genl_ctrl_alloc_cache(struct nl_sock *sk, struct nl_cache **result) """

#noinspection PyUnusedLocal
@wrap_ptr(genl, c_nl_cache_p, c_int)
def genl_ctrl_search(cache, id):
    """ struct genl_family *genl_ctrl_search(struct nl_cache *, int id); """

#noinspection PyUnusedLocal
@wrap_ptr(genl, c_nl_cache_p, c_char_p)
def genl_ctrl_search_by_name(cache, name):
    """  struct genl_family *genl_ctrl_search_by_name(struct nl_cache *cache, const char *name) """

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

        xxx = c_nl_cache_p()
        genl_ctrl_alloc_cache(sock, byref(xxx))
        super(CtrlCache, self).__init__(xxx, None)
        self._sock = sock # prevent from garbage collecting
        self._need_free = True

    def search_by_name(self, name):
        ptr = genl_ctrl_search_by_name(self, name)
        return Family(ptr=ptr, parent=self)

    def search(self, id):
        ptr = genl_ctrl_search(self, id)
        return Family(ptr=ptr, parent=self)
