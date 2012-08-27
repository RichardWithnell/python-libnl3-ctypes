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

class AttrIterator(object):
    """
    #define nlmsg_for_each_attr in original .h file
    """

    def __init__(self, genhdr):
        self.genhdr = genhdr
        self.obj = None
        self.rem = None

    def __next__(self):
        if self.obj is None:
            rem = self.genhdr.genlmsg_attrlen()
            pos = self.genhdr.genlmsg_attrdata()
        else:
            rem = c_int(self.rem)
            pos = self.obj.nla_next(byref(rem))

        if not pos.nla_ok(rem):
            raise StopIteration()
        self.obj = pos
        self.rem = rem
        return pos

    next = __next__

c_genlmsghdr_p = c_void_p
class GenlMsgHdr_nohdrlen(object):
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

class GenlMsgHdr(GenlMsgHdr_nohdrlen):
    def __init__(self, ptr, message, hdrlen=None):
        super(GenlMsgHdr, self).__init__(ptr, message)
        if hdrlen is not None:
            self.hdrlen = hdrlen

    def genlmsg_attrdata(self):
        return super(GenlMsgHdr, self).genlmsg_attrdata(self.hdrlen)

    def genlmsg_attrlen(self):
        return super(GenlMsgHdr, self).genlmsg_attrlen(self.hdrlen)

    def __iter__(self):
        return AttrIterator(self)
