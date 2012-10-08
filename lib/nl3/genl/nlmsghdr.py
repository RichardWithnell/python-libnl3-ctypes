#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_void_p
from .genl_msghdr import GenlMsgHdr
from ...import  wrap_int, wrap_ptr_no_check
from ..nlmsghdr import NlMsgHdr as _NlMsgHdr, nlmsg_data
from .import genl

c_nlmsghdr_p = c_void_p
c_genlmsghdr_p = c_void_p

#noinspection PyUnusedLocal
@wrap_int(genl, c_nlmsghdr_p, c_int)
def genlmsg_valid_hdr(nlh, hdrlen):
    """int genlmsg_valid_hdr(struct nlmsghdr * nlh, int hdrlen)"""

try:
    #noinspection PyUnusedLocal
    @wrap_ptr_no_check(genl, c_genlmsghdr_p)
    def genlmsg_hdr(nlh):
        """ struct genlmsghdr* genlmsg_hdr(struct nlmsghdr * nlh) """

except AttributeError:
    #noinspection PyRedeclaration
    def genlmsg_hdr(nlh):
        return nlmsg_data(nlh)

class NlMsgHdr(_NlMsgHdr):
    _GenlMsgHdr_class = GenlMsgHdr

    def __init__(self, ptr, parent):
        super(NlMsgHdr, self).__init__(ptr, parent)

    def hdr(self):
        ptr = genlmsg_hdr(self)
        return self._GenlMsgHdr_class(ptr=ptr, parent=self)

    def valid_hdr(self):
        return bool(genlmsg_valid_hdr(self, self._GenlMsgHdr_class._hdrlen))
