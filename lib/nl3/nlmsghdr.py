#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from ctypes import  c_void_p, c_int
from .import nl
from .attribute import Attribute
from ..import wrap_ptr_no_check, wrap_int

c_nlmsghdr_p = c_void_p

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nlmsghdr_p)
def nlmsg_data(nlh):
    """void * nlmsg_data (const struct nlmsghdr *nlh)"""

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nlmsghdr_p, c_int)
def nlmsg_attrdata(nlh, hdrlen):
    """ struct nlattr *nlmsg_attrdata(const struct nlmsghdr *nlh, int hdrlen) """

#noinspection PyUnusedLocal
@wrap_int(nl, c_nlmsghdr_p, c_int)
def nlmsg_attrlen(nlh, hdrlen):
    """ int nlmsg_attrlen(const struct nlmsghdr *nlh, int hdrlen) """


class NlMsgHdr(object):
    _attr_class = Attribute

    def __init__(self, ptr, parent):
        if ptr is not None:
            self._as_parameter_ = ptr
            self._parent = parent
            return
        raise NotImplementedError('ptr is None')

    data = lambda self: nlmsg_data(self)
    attrlen = lambda self, hdrlen: nlmsg_attrlen(self, hdrlen)

    def attrdata(self, hdrlen):
        attr = nlmsg_attrdata(self, hdrlen)
        return self._attr_class(ptr=attr, parent=self)

    def attributes(self, hdrlen):
        """
        #define nlmsg_for_each_attr in original .h file
        """
        pos = self.attrdata(hdrlen)
        rem = self.attrlen(hdrlen)
        while pos.ok(rem):
            yield pos
            (pos, rem) = pos.next(rem)
