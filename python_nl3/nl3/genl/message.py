#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_uint32, c_uint8, c_void_p
from .nlmsghdr import NlMsgHdr
from ... import nullptr_check
from .. import wrap
from ..message import Message as _Message
from ..message import c_nl_msg_p

from . import genl

class Message(_Message):
    _NlMsgHdr_class = NlMsgHdr
    @wrap(genl, nullptr_check, c_void_p, c_nl_msg_p, c_uint32, c_uint32, c_int, c_int, c_int, c_uint8, c_uint8)
    def genlmsg_put(): pass
