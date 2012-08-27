#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from ctypes import c_int, c_char_p, POINTER, byref
from . import genl
from .genl_family import c_genl_family_p, Family

from ... import swrap, nullptr_check
from .. import errcode_check, fwrap

from ..socket import c_nl_sock_p, Socket
from ..cache import NlCache, c_nl_cache_p, cache_name2class


@swrap(genl, errcode_check, c_int, c_nl_sock_p, POINTER(c_nl_cache_p))
def genl_ctrl_alloc_cache():
    """genl_ctrl_alloc_cache(struct nl_sock *, struct nl_cache **);"""

cache_name = 'genl/family'

class CtrlCache(NlCache):
    def __init__(self, arg):
        if isinstance(arg, Socket):
            sock = arg
            self.socket = sock # prevent fropm garbage collecting
            xxx = c_nl_cache_p()
            self._alloc_ptr = lambda : xxx if genl_ctrl_alloc_cache(sock, byref(xxx)) else xxx
            super(CtrlCache, self).__init__()
            return
        if isinstance(arg, c_nl_cache_p):
            super(CtrlCache, self).__init__(arg)
            return
        raise ValueError('Unknown argument passed to constructor: %r', arg)

    @fwrap(genl, nullptr_check, c_genl_family_p, c_nl_cache_p, c_int)
    def genl_ctrl_search(self, result):
        """ struct genl_family *     genl_ctrl_search(struct nl_cache *, int); """
        return Family(result, self)

    @fwrap(genl, nullptr_check, c_genl_family_p, c_nl_cache_p, c_char_p)
    def genl_ctrl_search_by_name(self, result):
        """struct genl_family *     genl_ctrl_search_by_name(struct nl_cache *, const char *);"""
        return Family(result, self)

cache_name2class[cache_name] = CtrlCache
