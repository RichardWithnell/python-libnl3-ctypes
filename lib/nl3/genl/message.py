#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ...ctypes.libnl3_genl import genlmsg_put
from ..message import Message as _Message
from .nlmsghdr import NlMsgHdr


class Message(_Message):
    _NlMsgHdr_class = NlMsgHdr

    put = lambda self, port, seq, family, hdrlen, flags, cmd, version: genlmsg_put(self, port, seq, family, hdrlen,
        flags, cmd, version)
