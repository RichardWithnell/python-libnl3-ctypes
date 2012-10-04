#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_uint32, c_uint8, c_void_p
from ...import wrap_ptr
from ..message import Message as _Message
from .nlmsghdr import NlMsgHdr
from .import genl

c_nl_msg_p = c_void_p

#noinspection PyUnusedLocal
@wrap_ptr(genl, c_nl_msg_p, c_uint32, c_uint32, c_int, c_int, c_int, c_uint8, c_uint8)
def genlmsg_put(msg, port, seq, family, hdrlen, flags, cmd, version):
    """ void *genlmsg_put(struct nl_msg *msg, uint32_t port, uint32_t seq, int family, int hdrlen, int flags, uint8_t cmd, uint8_t version) """


class Message(_Message):
    _NlMsgHdr_class = NlMsgHdr

    put = lambda self, port, seq, family, hdrlen, flags, cmd, version: genlmsg_put(self, port, seq, family, hdrlen,
        flags, cmd, version)
