#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_void_p, CFUNCTYPE
from . import nl, wrap, fwrap
from .. import StdNL, swrap
from .nlobject import NlObject, c_nl_object_p

c_nl_cache_p = c_void_p

@swrap(nl, None, None, c_nl_cache_p)
def nl_cache_free():
    """     void nl_cache_free(struct nl_cache * cache) """

_foreach_cbtype = CFUNCTYPE(None, c_nl_cache_p, c_void_p)

@swrap(nl, None, None, c_nl_cache_p, _foreach_cbtype, c_void_p)
def nl_cache_foreach():
    """ nl_cache_foreach(cache, callback, NULL);"""

class CacheIterator(object):
    def __init__(self, cache):
        self._cache = cache
        self._object = None

    def __next__(self):
        if self._object is None:
            self._object = self._cache.nl_cache_get_first()
        else:
            self._object = self._object.nl_cache_get_next()
        if self._object is None:
            raise StopIteration()
        return self._object

    next = __next__

class NlCache(StdNL):
    _free_ptr = nl_cache_free

    _objclass = NlObject

    def nl_cache_foreach(self, callback):
        def c_callback(obj, _void_ptr):
            return callback(self._objclass(obj, self))

        nl_cache_foreach(self, _foreach_cbtype(c_callback), None)

    @fwrap(nl, None, c_nl_object_p, c_nl_cache_p)
    def nl_cache_get_first(self, result):
        if not result:
            return None
        else:
            return self._objclass(result, self)

    def __iter__(self):
        return CacheIterator(self)
