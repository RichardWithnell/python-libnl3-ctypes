#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from .attribute import Attribute
from lib.ctypes.libnl3.msg import nlmsg_data, nlmsg_attrdata, nlmsg_attrlen


class NlMsgHdr(object):
    _attr_class = Attribute

    def __init__(self, ptr, parent):
        if ptr is None:
            raise NotImplementedError('ptr is None')
        self._as_parameter_ = ptr
        self._parent = parent

    data = lambda self: nlmsg_data(self)
    attrlen = lambda self, hdrlen: nlmsg_attrlen(self, hdrlen)

    def attrdata(self, hdrlen):
        """
        :type hdrlen: int
        """
        attr = nlmsg_attrdata(self, hdrlen)
        return self._attr_class(ptr=attr, parent=self)

    def attributes(self, hdrlen):
        """
        Yields of enclosed attributes
        #define nlmsg_for_each_attr in original .h file

        :type hdrlen: int
        """
        pos = self.attrdata(hdrlen)  # returns Attribute (sub)class
        rem = self.attrlen(hdrlen)
        while pos.ok(rem):
            yield pos
            (pos, rem) = pos.next(rem)
        if rem:
            raise RuntimeError('Extra data after nlmsg attributes')
