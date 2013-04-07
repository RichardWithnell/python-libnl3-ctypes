# coding=utf-8

from __future__ import absolute_import
from _ctypes import POINTER
from ctypes import c_char_p, c_void_p, c_int, CFUNCTYPE
from ...ctypes import wrap_ptr_no_check, wrap_void
from . import nl, c_nl_object_p, wrap_ret_last_dbl_ptr, wrap_nl_err, c_nl_cache_mngr_p, c_nl_cache_p, c_nl_sock_p


NL_AUTO_PROVIDE = 1

# typedef void (*change_func_t)(struct nl_cache *, struct nl_object *, int, void *);
change_func_t = CFUNCTYPE(None, c_nl_cache_p, c_nl_object_p, c_void_p)


@wrap_ptr_no_check(nl, c_nl_object_p)
def nl_cache_get_next(obj):
    """ struct nl_object *nl_cache_get_next(struct nl_object *obj) """


@wrap_ret_last_dbl_ptr
@wrap_nl_err(nl, c_nl_cache_mngr_p, c_char_p, change_func_t, c_void_p, POINTER(c_nl_cache_p))
def nl_cache_mngr_add(mngr, name, callback, data):
    """int nl_cache_mngr_add(struct nl_cache_mngr * mngr,
    const char * name,
    change_func_t cb,
    void * data,
    struct nl_cache ** result
    )"""


@wrap_void(nl, c_nl_cache_mngr_p)
def nl_cache_mngr_free(mngr):
    """void nl_cache_mngr_free(struct nl_cache_mngr * mngr)"""


@wrap_ret_last_dbl_ptr
@wrap_nl_err(nl, c_nl_sock_p, c_int, c_int, POINTER(c_nl_cache_mngr_p))
def nl_cache_mngr_alloc(sock, protocol, flags):
    """
    int nl_cache_mngr_alloc(struct nl_sock * sk,
    int protocol,
    int flags,
    struct nl_cache_mngr ** result
    )"""


@wrap_ptr_no_check(nl, c_nl_cache_p)
def nl_cache_get_first(cache):
    """ struct nl_object *nl_cache_get_first(struct nl_cache *cache) """


@wrap_void(nl, c_nl_cache_p)
def nl_cache_free(cache):
    """     void nl_cache_free(struct nl_cache * cache) """