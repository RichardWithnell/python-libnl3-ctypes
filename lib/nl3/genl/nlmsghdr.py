#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ...ctypes.libnl3_genl import *
from ..nlmsghdr import NlMsgHdr as _NlMsgHdr
from .genl_msghdr import GenlMsgHdr

class NlMsgHdr(_NlMsgHdr):
    _GenlMsgHdr_class = GenlMsgHdr

    def __init__(self, ptr, parent):
        super(NlMsgHdr, self).__init__(ptr, parent)

    def hdr(self):
        ptr = genlmsg_hdr(self)
        return self._GenlMsgHdr_class(ptr=ptr, parent=self)

    def valid_hdr(self):
        return bool(genlmsg_valid_hdr(self, self._GenlMsgHdr_class._hdrlen))
