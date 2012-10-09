#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

import traceback
from ctypes import  byref

from ..ctypes.libnl3 import *
from .socket import Socket


#TODO: override __new__ to return same instance if same pointer value returned.
#Also, FILE(libc.stdin) should not generate new instance...

class CacheMgr(object):
    def __init__(self, protocol, sock=None, flags=NL_AUTO_PROVIDE):
        """ protocol is like NETLINK_GENERIC"""
        #        if sock is None and version < 3.2.8:
        #            raise UnimplementedError('Too old libnl version. It does not support automatic socket allocation')
        self._need_free = False
        if sock is None:
            sock = Socket()
            #sock.nl_connect(protocol)

        self.__sock = sock # prevent from socket garbage collection

        cache = c_nl_cache_mngr_p()
        nl_cache_mngr_alloc(sock, protocol, flags, byref(cache))
        self._as_parameter_ = cache
        self._need_free = True

    def _free(self):
        nl_cache_mngr_free(self)
        del self._as_parameter_

    def __del__(self):
        if self._need_free:
            self._free()
            self._need_free = False


    # TODO: def add(self, name, cacheclass) ? instead of callback, call self.on_change(object). So, user should
    # TODO: create class(genl.taskstats_cache). we will get class._name to pass to C API
    def add(self, cls):
        #noinspection PyUnusedLocal
        def c_callback(_cache, obj, _ptr):
            #noinspection PyBroadException
            try:
                if _cache != cache_instance._as_parameter_:
                    raise RuntimeError('Different cache passed to callback')
                cache_instance.on_change(cache_instance._objclass(ptr=obj, parent=cache_instance))
            except:
                traceback.print_exc()

        if hasattr(cls, 'on_change'):
            cb = change_func_t(c_callback)
        else:
            cb = None
        xxx = c_nl_cache_p()
        nl_cache_mngr_add(self, cls._cache_name, cb, None, byref(xxx))
        cache_instance = cls(xxx)
        return cache_instance
