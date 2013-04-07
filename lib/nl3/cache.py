#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from lib.ctypes.libnl3.cache import nl_cache_get_first, nl_cache_free
from .nlobject import NlObject


class NlCache(object):
    _objclass = NlObject

    def __init__(self, ptr=None, parent=None):
        self._need_free = False
        if ptr is None:
            raise NotImplementedError('NlCache allocation is not implemented')
        self._as_parameter_ = ptr
        self._parent = parent

    def _free(self):
        nl_cache_free(self)
        del self._as_parameter_

    def __del__(self):
        if self._need_free:
            self._free()
            self._need_free = False

    def _get_first(self):
        """ Returns NlObject subclass """
        obj = nl_cache_get_first(self)
        if not obj:
            raise StopIteration()
        return self._objclass(ptr=obj, parent=self)

    def __iter__(self):
        """ Yields objects in cache """
        obj = self._get_first()
        yield obj

        while 1:
            obj = obj.get_next()
            yield obj
