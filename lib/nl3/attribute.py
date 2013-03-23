#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from ..ctypes.libnl3 import *


class Attribute(object):
    def __init__(self, ptr=None, parent=None):
        self._parent = parent
        self._as_parameter_ = ptr

    #TODO: make them property
    ok = lambda self, len: bool(nla_ok(self, len))
    data = lambda self: nla_data(self)
    len = lambda self: nla_len(self)
    type = lambda self: nla_type(self)

    u32 = property(nla_get_u32)
    u64 = property(nla_get_u64)

    def next(self, remainig):
        # never return NULL
        (attr, remainig) = nla_next(self, remainig)
        return (Attribute(ptr=attr, parent=self._parent), remainig)

    def attributes(self):
        attr = Attribute(ptr=self.data(), parent=self._parent)
        len = self.len()
        while attr.ok(len):
            yield attr
            (attr, len) = attr.next(len)
