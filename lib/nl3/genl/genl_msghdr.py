#!/usr/bin/env python
# coding: utf-8


from __future__ import absolute_import

from ...ctypes.libnl3_genl import *
from ..attribute import Attribute


class GenlMsgHdr(object):
    # TODO: this is abstract class
    _family_hdrlen = None
    _family_id = None
    _version = None

    def __init__(self, ptr, parent):
        if ptr is None:
            raise NotImplementedError('ptr is None')
        self._as_parameter_ = ptr
        self._parent = parent

    data = lambda self: genlmsg_data(self)

    def attrdata(self):
        ptr = genlmsg_attrdata(self, self._family_hdrlen)
        return Attribute(ptr=ptr, parent=self)

    attrlen = lambda self: genlmsg_attrlen(self, self._family_hdrlen)

    def __iter__(self):
        rem = self.attrlen()
        pos = self.attrdata()
        while pos.ok(rem):
            yield pos
            (pos, rem) = pos.next(rem)
        if rem:
            raise RuntimeError('Extra data after genlmsg attributes')
