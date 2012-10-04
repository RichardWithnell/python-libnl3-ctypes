#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_void_p
from ..import wrap_nl_err
from ..socket import Socket as _Socket
from .import genl, NETLINK_GENERIC
from .message import Message

c_nl_sock_p = c_void_p

#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p)
def genl_connect(sock):
    """ int genl_connect(struct nl_sock *sk) """

#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p, c_int, c_int, c_int, c_int)
def genl_send_simple(sock, family, cmd, version, flags):
    """ int genl_send_simple(struct nl_sock *sk, int family, int cmd, int version, int flags) """


class Socket(_Socket):
    _message_class = Message
    _protocol = NETLINK_GENERIC

    connect = lambda self: genl_connect(self)
    send_simple = lambda self, family, cmd, version, flags: genl_send_simple(self, family, cmd, version, flags)
