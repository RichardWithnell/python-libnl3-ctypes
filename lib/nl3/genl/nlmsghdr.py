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
    def hdr(self, hdrlen):
        ptr = genlmsg_hdr(self)
        return GenlMsgHdr(ptr=ptr, parent=self, hdrlen=hdrlen)

    #    def genlmsg_hdr(self, hdrlen=None):
    #        ghdr = super(NlMsgHdr, self).genlmsg_hdr()
    #
    #        if hdrlen is None:
    #            hdrlen = getattr(self, '_family_hdrsize', None)
    #
    #        if hdrlen is None:
    #            raise Exception('Header size is not known')
    #
    #        ghdr.hdrlen = hdrlen
    #        return ghdr

    valid_hdr = lambda self, hdrlen: bool(genlmsg_valid_hdr(self, hdrlen))

#
#    def genlmsg_valid_hdr(self, hdrlen=None):
#        if hdrlen is None:
#            hdrlen = getattr(self, '_family_hdrsize', None)
#
#        if hdrlen is None:
#            raise Exception('Header size is not known')
#
#        return super(NlMsgHdr, self).genlmsg_valid_hdr(hdrlen)