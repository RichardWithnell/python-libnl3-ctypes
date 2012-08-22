#!/usr/bin/env python
# coding: utf-8

#TODO:
# c_int  vs c_bool
# c_bool vs Exception

from __future__ import absolute_import

from ctypes import byref, c_void_p, c_int
from . import genl
from ... import nullptr_check
from .. import wrap, fwrap
from ..attribute import Attribute

c_genlmsghdr_p = c_void_p
class GenlMsgHdr(object):
    def __init__(self, ptr, message):
        self._message_link = message # prevent from message garbage collection
        self._as_parameter_ = ptr

    @fwrap(genl, nullptr_check, c_genlmsghdr_p, c_int)
    def genlmsg_attrdata(self, result):
        """
            struct nlattr* genlmsg_attrdata(const struct genlmsghdr * gnlh,
            int hdrlen)"""
        return Attribute(result, self)

    @wrap(genl, None, c_int, c_genlmsghdr_p, c_int)
    def genlmsg_attrlen():
        """int genlmsg_attrlen(const struct genlmsghdr * gnlh,
        int hdrlen)"""

    @wrap(genl, nullptr_check, c_void_p, c_genlmsghdr_p)
    def genlmsg_data():
        """void* genlmsg_data(const struct genlmsghdr * gnlh)"""

    @wrap(genl, None, c_int, c_genlmsghdr_p, c_int)
    def genlmsg_valid_hdr():
        """ int genlmsg_valid_hdr(struct nlmsghdr * nlh,
            int hdrlen)"""

    def attributes(self, hdrlen):
        """
        #define nlmsg_for_each_attr in original .h file
        """
        pos = self.genlmsg_attrdata(hdrlen)
        rem = c_int(self.genlmsg_attrlen(hdrlen))
        while pos.nla_ok(rem):
            yield pos
            pos = pos.nla_next(byref(rem))
