#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ...ctypes.libnl3_genl import *
from ..socket import Socket as _Socket
from .message import Message

class Socket(_Socket):
    _message_class = Message
    _protocol = NETLINK_GENERIC

    connect = lambda self: genl_connect(self)
    send_simple = lambda self, family, cmd, version, flags: genl_send_simple(self, family, cmd, version, flags)
