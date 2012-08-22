#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_bool
from .genl_msghdr import c_genlmsghdr_p, GenlMsgHdr
from ... import nullptr_check
from .. import wrap, fwrap
from ..nlmsghdr import NlMsgHdr as _NlMsgHdr
from ..nlmsghdr import c_nlmsghdr_p
from . import genl

class NlMsgHdr(_NlMsgHdr):

    # return c_int in original
    @wrap(genl, None, c_bool, c_nlmsghdr_p, c_int)
    def genlmsg_valid_hdr():
        """int genlmsg_valid_hdr(struct nlmsghdr * nlh,
            int hdrlen)"""

    try:
        @fwrap(genl, nullptr_check, c_genlmsghdr_p)
        def genlmsg_hdr(self, result):
            """ struct genlmsghdr* genlmsg_hdr(struct nlmsghdr * nlh) """
            return GenlMsgHdr(result, self)
    except AttributeError:
        def genlmsg_hdr(self):
            """
            struct genlmsghdr *genlmsg_hdr(struct nlmsghdr *nlh)
            {
                return nlmsg_data(nlh);
            }
            """
            return GenlMsgHdr(self.nlmsg_data(), self)
