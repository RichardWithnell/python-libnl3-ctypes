#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int
from .. import errcode_check, wrap
from ..socket import Socket as _Socket
from ..socket import c_socket_p
from . import genl
from .message import Message

class Socket(_Socket):
    _message_class = Message

    @wrap(genl, errcode_check, c_int, c_socket_p)
    def genl_connect(): pass

    @wrap(genl, errcode_check, c_int, c_socket_p, c_int, c_int, c_int, c_int)
    def genl_send_simple(): pass
