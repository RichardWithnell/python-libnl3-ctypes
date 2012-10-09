#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from ..ctypes.libnl3 import *
from .attribute import Attribute


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
