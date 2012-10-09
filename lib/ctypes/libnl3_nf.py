#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_void_p, c_int, c_uint64, c_uint8, c_uint16, POINTER
from .import MYDLL, wrap_int, wrap_custom, wrap_ptr
from .libnl3 import wrap_nl_err

NETLINK_NETFILTER = 12

nfnl = MYDLL('libnl-nf-3.so.200')

c_nfnl_ct_p = c_void_p
c_nl_sock_p = c_void_p
c_nl_cache_p = c_void_p

#noinspection PyUnusedLocal
@wrap_int(nfnl, c_nfnl_ct_p, c_int)
def nfnl_ct_test_packets(ct, direction):
    pass

#noinspection PyUnusedLocal
@wrap_int(nfnl, c_nfnl_ct_p, c_int)
def nfnl_ct_test_bytes(ct, direction):
    pass

#noinspection PyUnusedLocal
@wrap_custom(nfnl, c_uint64, c_nfnl_ct_p, c_int)
def nfnl_ct_get_packets(ct, direction):
    pass

#noinspection PyUnusedLocal
@wrap_custom(nfnl, c_uint64, c_nfnl_ct_p, c_int)
def nfnl_ct_get_bytes(ct, direction):
    pass

#########################################################################


#noinspection PyUnusedLocal
@wrap_nl_err(nfnl, c_nl_sock_p, POINTER(c_nl_cache_p))
def nfnl_ct_alloc_cache(sock, cache_p):
    """nfl_alloc_cache(struct nl_sock *, struct nl_cache **);"""


#########################################################################

#noinspection PyUnusedLocal
@wrap_ptr(nfnl, c_uint8, c_uint8, c_int, c_uint8, c_uint16)
def nfnlmsg_alloc_simple(subsys_id, type, flags, family, res_id):
    """
    struct nl_msg* nfnlmsg_alloc_simple     (       uint8_t         subsys_id,
    uint8_t         type,
    int     flags,
    uint8_t         family,
    uint16_t        res_id
    )"""

#########################################################################

#noinspection PyUnusedLocal
@wrap_nl_err(nfnl, c_nl_sock_p)
def nfnl_connect(sock):
    """ int nfnl_connect(struct nl_sock *sk) """

#########################################################################

