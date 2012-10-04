#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_void_p
from .import nl
from ..import  wrap_void, wrap_ptr_no_check
from .nlobject import NlObject

c_nl_cache_p = c_void_p

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_cache_p)
def nl_cache_free(cache):
    """     void nl_cache_free(struct nl_cache * cache) """


#_foreach_cbtype = CFUNCTYPE(None, c_nl_cache_p, c_void_p)
##noinspection PyUnusedLocal
#@wrap_void(nl, c_nl_cache_p, _foreach_cbtype, c_void_p)
#def nl_cache_foreach(cache, callback, arg):
#    """ void nl_cache_foreach(struct nl_cache *cache, void (*cb)(struct nl_object *, void *), void *arg) """
#
#
#def nl_cache_foreach(cache, callback):
#    """ deprecated in python """
#    def c_callback(obj, _void_ptr):
#        try:
#            callback(self._objclass(obj, self))
#        except:
#            traceback.print_exc()
#
#    nl_cache_foreach(self, _foreach_cbtype(c_callback), None)
#

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nl_cache_p)
def nl_cache_get_first(cache):
    """ struct nl_object *nl_cache_get_first(struct nl_cache *cache) """


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
