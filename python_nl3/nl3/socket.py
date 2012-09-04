#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_void_p, CFUNCTYPE
from . import nl,  errcode_check, wrap
from .. import nullptr_check, StdNL, swrap
from .message import c_nl_msg_p, Message
import traceback

NL_CB_VALID = 0
NL_CB_CUSTOM = 3
NL_CB_MSG_IN = 5

NL_OK = 0
NL_STOP = 2

c_nl_sock_p = c_void_p

@swrap(nl, nullptr_check, c_nl_sock_p)
def nl_socket_alloc(): pass

@swrap(nl, None, None, c_nl_sock_p)
def nl_socket_free():
    """ Close file desriptor and free memory """

@swrap(nl, errcode_check, c_int, c_nl_sock_p, c_int, c_int, c_void_p, c_void_p)
def nl_socket_modify_cb():
    """
    int nl_socket_modify_cb(struct nl_sock * sk,
    enum nl_cb_type type,
    enum nl_cb_kind kind,
    nl_recvmsg_msg_cb_t func,
    void * arg 
    )
    """

_cbtype = CFUNCTYPE(c_int, c_nl_msg_p, c_void_p)
arr = []
class Socket(StdNL):
    """
    Low-level libnl interface
    """
    _alloc_ptr = nl_socket_alloc
    _free_ptr = nl_socket_free
    _message_class = Message
    _protocol = None

    def nl_socket_modify_cb(self, type_, kind, func):
        msgcls = self._message_class
        def c_callback(msg, _void_ptr):
            try:
                ret = func(msgcls(msg))
                return NL_OK if ret is None else int(ret)
            except:
                traceback.print_exc()
                return NL_STOP
        qwe = _cbtype(c_callback)
        arr.append(qwe)
        return nl_socket_modify_cb(self, type_, kind, qwe, None)

    @wrap(nl, None, c_int, c_nl_sock_p)
    def nl_socket_get_fd(): pass

    @wrap(nl, errcode_check, c_int, c_nl_sock_p, c_nl_msg_p)
    def nl_send_auto_complete(): pass

    @wrap(nl, errcode_check, c_int, c_nl_sock_p)
    def nl_recvmsgs_default(): pass

    @wrap(nl, None, None, c_nl_sock_p)
    def nl_socket_disable_seq_check(): pass

    @wrap(nl, errcode_check, c_int, c_nl_sock_p)
    def nl_socket_set_nonblocking(): pass

    @wrap(nl, errcode_check, c_int, c_nl_sock_p)
    def nl_wait_for_ack(): pass

    @wrap(nl, None, None, c_nl_sock_p)
    def nl_close():
        """ Just close file descriptor, not free memory """

    @wrap(nl, errcode_check, c_int, c_nl_sock_p, c_int)
    def nl_connect():
        """ int nl_connect(struct nl_sock * sk, int protocol) """

    def __enter__(self):
        if self._protocol is None:
            raise Exception('Unknown family, so can not connect automagically')
        self.nl_connect(self._protocol)
        return self

    def __exit__(self, type, value, tb):
        self.nl_close()

    def fileno(self):
        return self.nl_socket_get_fd()
