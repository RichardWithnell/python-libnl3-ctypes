#!/usr/bin/env python
# coding: utf-8


from __future__ import absolute_import

from ctypes import  c_void_p, c_int
from ...import wrap_ptr_no_check, wrap_int
from ..attribute import Attribute
from .import genl

c_genlmsghdr_p = c_void_p

#noinspection PyUnusedLocal
@wrap_ptr_no_check(genl, c_genlmsghdr_p, c_int)
def genlmsg_attrdata(gnlh, hdrlen):
    """ struct nlattr* genlmsg_attrdata(const struct genlmsghdr * gnlh, int hdrlen)"""

#noinspection PyUnusedLocal
@wrap_int(genl, c_genlmsghdr_p, c_int)
def genlmsg_attrlen(gnlh, hdrlen):
    """int genlmsg_attrlen(const struct genlmsghdr * gnlh, int hdrlen)"""

#noinspection PyUnusedLocal
@wrap_ptr_no_check(genl, c_genlmsghdr_p)
def genlmsg_data(gnlh):
    """void* genlmsg_data(const struct genlmsghdr * gnlh)"""


class GenlMsgHdr(object):
    _hdrlen = 0

    def __init__(self, ptr, parent):
        if ptr is not None:
            self._as_parameter_ = ptr
            self._parent = parent
            return
        raise NotImplementedError('ptr is None')

    data = lambda self: genlmsg_data(self)

    def attrdata(self):
        ptr = genlmsg_attrdata(self, self._hdrlen)
        return Attribute(ptr=ptr, parent=self)

    attrlen = lambda self: genlmsg_attrlen(self, self._hdrlen)

    def __iter__(self):
        rem = self.attrlen()
        pos = self.attrdata()
        while pos.ok(rem):
            yield pos
            (pos, rem) = pos.next(rem)
        if rem:
            raise RuntimeError('Extra data after genlmsg attributes')
