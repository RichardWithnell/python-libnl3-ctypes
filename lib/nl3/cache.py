#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from ..ctypes.libnl3 import *
from .nlobject import NlObject


class NlCache(object):
    _objclass = NlObject

    def __init__(self, ptr=None, parent=None):
        self._need_free = False
        self._as_parameter_ = ptr
        self._parent = parent

    def _free(self):
        nl_cache_free(self)
        del self._as_parameter_

    def __del__(self):
        if self._need_free:
            self._free()
            self._need_free = False

    def get_first(self):
        obj = nl_cache_get_first(self)
        if obj == 0:
            raise StopIteration()
        return self._objclass(ptr=obj, parent=self)


    def __iter__(self):
        obj = self.get_first()
        yield obj

        while 1:
            obj = obj.get_next()
            yield obj
