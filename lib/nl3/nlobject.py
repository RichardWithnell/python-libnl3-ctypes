#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from .import nl
from ..import wrap_ptr_no_check
from ctypes import c_void_p

c_nl_object_p = c_void_p

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nl_object_p)
def nl_cache_get_next(obj):
    """ struct nl_object *nl_cache_get_next(struct nl_object *obj) """


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
