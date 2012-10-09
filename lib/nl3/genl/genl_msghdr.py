#!/usr/bin/env python
# coding: utf-8


from __future__ import absolute_import

from ...ctypes.libnl3_genl import *
from ..attribute import Attribute

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
