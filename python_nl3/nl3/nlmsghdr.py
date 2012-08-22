#!/usr/bin/env python
# coding: utf-8

#TODO:
# c_int  vs c_bool
# c_bool vs Exception

from __future__ import absolute_import

from ctypes import byref, c_void_p, c_int
from . import nl, wrap, fwrap
from .. import nullptr_check
from .attribute import Attribute, c_nlattr_p

c_nlmsghdr_p = c_void_p
class NlMsgHdr(object):
    def __init__(self, ptr, message):
        self._message_link = message # prevent from message garbage collection
        self._as_parameter_ = ptr

    @wrap(nl, nullptr_check, c_nlmsghdr_p)
    def nlmsg_data():
        """nlmsg_data (const struct nlmsghdr *nlh)"""


    @fwrap(nl, nullptr_check, c_nlattr_p, c_nlmsghdr_p, c_int)
    def nlmsg_attrdata(self, result):
        """struct nlattr* nlmsg_attrdata(const struct nlmsghdr * nlh,
            int hdrlen
            )"""
        return Attribute(result, self)

    @wrap(nl, None, c_int, c_nlmsghdr_p, c_int)
    def nlmsg_attrlen():
        """int nlmsg_attrlen(const struct nlmsghdr * nlh,
            int hdrlen
            )"""

    def attributes(self, hdrlen):
        """
        #define nlmsg_for_each_attr in original .h file
        """
        pos = self.nlmsg_attrdata(hdrlen)
        rem = c_int(self.nlmsg_attrlen(hdrlen))
        while pos.nla_ok(rem):
            yield pos
            pos = pos.nla_next(byref(rem))
