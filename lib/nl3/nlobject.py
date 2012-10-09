#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from ..ctypes.libnl3 import nl_cache_get_next


class NlObject(object):
    def __init__(self, ptr=None, parent=None):
        if ptr is not None:
            self._as_parameter_ = ptr
            self._parent = parent # prevent from parent garbage collection
            return
        raise NotImplementedError('ptr is None')

    def get_next(self):
        next = nl_cache_get_next(self)
        if next == 0:
            raise StopIteration()
        return self.__class__(ptr=next, parent=self._parent)
