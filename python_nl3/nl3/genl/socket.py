#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_char_p
from .. import errcode_check, wrap
from ..socket import Socket as _Socket
from ..socket import c_socket_p
from . import genl, NETLINK_GENERIC
from .message import Message

class Socket(_Socket):
    _message_class = Message
    _protocol = NETLINK_GENERIC

    @wrap(genl, errcode_check, c_int, c_socket_p)
    def genl_connect(): pass

    @wrap(genl, errcode_check, c_int, c_socket_p, c_int, c_int, c_int, c_int)
    def genl_send_simple(): pass

    @wrap(genl, errcode_check, c_int, c_socket_p, c_char_p)
    def genl_ctrl_resolve():
        """int genl_ctrl_resolve(struct nl_sock *, const char *); """

    @wrap(genl, errcode_check, c_int, c_socket_p, c_char_p, c_char_p)
    def genl_ctrl_resolve_grp():
        """int genl_ctrl_resolve_grp(struct nl_sock *sk,
          const char *family,
          const char *grp);"""

