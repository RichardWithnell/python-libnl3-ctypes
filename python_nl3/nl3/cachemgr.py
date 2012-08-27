#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from .. import swrap, StdNL
from . import nl, errcode_check
from .socket import c_nl_sock_p, Socket
from .cache import c_nl_cache_p, cache_name2class
from .nlobject import c_nl_object_p

from ctypes import c_void_p, c_char_p, c_int, POINTER, CFUNCTYPE, byref

NL_AUTO_PROVIDE = 1

c_nl_cache_mngr_p = c_void_p

@swrap(nl, errcode_check, c_int, c_nl_sock_p, c_int, c_int, POINTER(c_nl_cache_mngr_p))
def nl_cache_mngr_alloc():
    """
    int nl_cache_mngr_alloc(struct nl_sock * sk,
    int protocol,
    int flags,
    struct nl_cache_mngr ** result
    )"""

@swrap(nl, None, None, c_nl_cache_mngr_p)
def nl_cache_mngr_free():
    """void nl_cache_mngr_free(struct nl_cache_mngr * mngr)"""

# typedef void (*change_func_t)(struct nl_cache *, struct nl_object *, int, void *);
change_func_t = CFUNCTYPE(None, c_nl_cache_p, c_nl_object_p, c_void_p)

@swrap(nl, errcode_check, c_int, c_nl_cache_mngr_p, c_char_p, change_func_t, c_void_p, POINTER(c_nl_cache_p))
def nl_cache_mngr_add():
    """int nl_cache_mngr_add(struct nl_cache_mngr * mngr,
    const char * name,
    change_func_t cb,
    void * data,
    struct nl_cache ** result
    )"""

class CacheMgr(StdNL):
    def __init__(self, sock, protocol, flags=NL_AUTO_PROVIDE):
        """ protocol is like NETLINK_GENERIC"""
#        if sock is None and version < 3.2.8:
#            raise UnimplementedError('Too old libnl version. It does not support automatic socket allocation')
        if sock is None:
            sock = Socket()
            #sock.nl_connect(protocol)

        self.sock = sock # prevent from socket garbage collection

        xxx = c_nl_cache_mngr_p()
        self._alloc_ptr = lambda : xxx if nl_cache_mngr_alloc(sock, protocol, flags, byref(xxx)) else xxx
        self._free_ptr = nl_cache_mngr_free
        super(CacheMgr, self).__init__()

    def nl_cache_mngr_add(self, name, callback=None):
        #TODO: reference counting ?!
        cacheclass = cache_name2class[name]
        if callback is not None:
            def c_callback(cache, obj, _ptr):
                try:
                    callback(cacheclass(cache), cacheclass._objclass(obj))
                except:
                    traceback.print_exc()
            cb = change_func_t(c_callback)
        else:
            cb = change_func_t(0)

        xxx = c_nl_cache_p()
        nl_cache_mngr_add(self, name, cb, None, byref(xxx))
        return cacheclass(xxx)
