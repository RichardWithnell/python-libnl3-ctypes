#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ...ctypes.libnl3_genl import genlmsg_put
from ..message import Message
from .nlmsghdr import NlMsgHdrGENL


class MessageGENL(Message):
    _NlMsgHdr_class = NlMsgHdrGENL

    #noinspection PyMethodOverriding
    def put(self, port, seq, flags, cmd):
        genhdr = self._NlMsgHdr_class._GenlMsgHdr_class
        genlmsg_put(self, port, seq, genhdr._family_id, genhdr._family_hdrlen, flags, cmd, genhdr._version)
