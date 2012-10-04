#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ctypes import c_int, c_char_p, POINTER, byref, c_void_p
from ....import wrap_ptr
from ...import wrap_nl_err
from ...cache import NlCache
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


class CtrlCache(NlCache):
    _cache_name = 'genl/family'

    def __init__(self, ptr=None, parent=None, sock=None):
        if ptr is not None:
            super(CtrlCache, self).__init__(ptr, parent)
            return
        if sock is None:
            raise ValueError('sock is None')
        xxx = c_nl_cache_p()
        ptr = genl_ctrl_alloc_cache(sock, byref(xxx))
        super(CtrlCache, self).__init__(ptr, sock)
        self._need_free = True

    def search_by_name(self, name):
        ptr = genl_ctrl_search_by_name(self, name)
        ret = Family(ptr=ptr)
        ret._need_free = True
        return ret

    def serach(self, id):
        ptr = genl_ctrl_search(self, id)
        ret = Family(ptr=ptr)
        ret._need_free = True
        return ret
