#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_void_p
from . import nl,  errcode_check, wrap
from .. import nullptr_check, StdNL, swrap
from .message import c_msg_p

NL_CB_MSG_IN = 5
NL_CB_CUSTOM = 3
NL_OK = 0
NL_STOP = 2

c_socket_p = c_void_p

@swrap(nl, nullptr_check, c_socket_p)
def nl_socket_alloc(): pass

@swrap(nl, None, None, c_socket_p)
def nl_socket_free(): pass

class Socket(StdNL):
    """
    Low-level libnl interface
    """
    _alloc_ptr = nl_socket_alloc
    _free_ptr = nl_socket_free

    @wrap(nl, errcode_check, c_int, c_socket_p, c_int, c_int, c_void_p, c_void_p)
    def nl_socket_modify_cb(): pass

    @wrap(nl, None, c_int, c_socket_p)
    def nl_socket_get_fd(): pass

    @wrap(nl, errcode_check, c_int, c_socket_p, c_msg_p)
    def nl_send_auto_complete(): pass

    @wrap(nl, errcode_check, c_int, c_socket_p)
    def nl_recvmsgs_default(): pass

    @wrap(nl, None, None, c_socket_p)
    def nl_socket_disable_seq_check(): pass

    @wrap(nl, errcode_check, c_int, c_socket_p)
    def nl_socket_set_nonblocking(): pass

    @wrap(nl, errcode_check, c_int, c_socket_p)
    def nl_wait_for_ack(): pass

    def fileno(self):
        return self.nl_socket_get_fd()
