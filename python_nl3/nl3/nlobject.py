#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from . import fwrap, nl
from .. import StdNL
from ctypes import c_void_p

c_nl_object_p = c_void_p

#TODO: alloc/free
class NlObject(StdNL):
    def __init__(self, ptr=None, cache=None):
        # create by known cache & c_void_p ptr
        if (ptr is not None) and (cache is not None):
            self._cache = cache # prevent from cache garbage collection
            super(NlObject, self).__init__(ptr)
            return

        # creation by known NlObject instance (copying constructor)
        if isinstance(ptr, NlObject) and (cache is None):
            self._cache = ptr._cache
            super(NlObject, self).__init__(ptr)
            return

        raise NotImplementedError(':)', ptr, cache)


    @fwrap(nl, None, c_nl_object_p, c_nl_object_p)
    def nl_cache_get_next(self, result):
        if not result:
            return None
        else:
            return self.__class__(result, self._cache)

