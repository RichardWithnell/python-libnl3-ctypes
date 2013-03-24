#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from ..ctypes.libnl3 import *


NLA_UNSPEC = 0  # /**< Unspecified type, binary data chunk */
NLA_U8 = 1      # /**< 8 bit integer */
NLA_U16 = 2     # /**< 16 bit integer */
NLA_U32 = 3     # /**< 32 bit integer */
NLA_U64 = 4     # /**< 64 bit integer */
NLA_STRING = 5  # /**< NUL terminated character string */
NLA_FLAG = 6    # /**< Flag */
NLA_MSECS = 7   # /**< Micro seconds (64bit) */
NLA_NESTED = 8  # /**< Nested attributes */


class Attribute(object):
    def __init__(self, ptr=None, parent=None):
        self._parent = parent
        self._as_parameter_ = ptr

    #TODO: make them property
    ok = lambda self, length: bool(nla_ok(self, length))
    data = lambda self: nla_data(self)
    len = lambda self: nla_len(self)
    type = lambda self: nla_type(self)

    u8 = property(nla_get_u8)
    u16 = property(nla_get_u16)
    u32 = property(nla_get_u32)
    u64 = property(nla_get_u64)

    @property
    def value(self):
        mytype = self.type
        if mytype == NLA_U8:
            return self.u8
        if mytype == NLA_U16:
            return self.u16
        if mytype == NLA_U32:
            return self.u32
        if mytype == NLA_U64:
            return self.u64
        raise NotImplementedError('Unknown my type', mytype)

    def next(self, remainig):
        # never return NULL
        (attr, remainig) = nla_next(self, remainig)
        return (Attribute(ptr=attr, parent=self._parent), remainig)

    def attributes(self):
        """ Yields of enclosed attributes """
        attr = Attribute(ptr=self.data(), parent=self._parent)
        len = self.len()
        while attr.ok(len):
            yield attr
            (attr, len) = attr.next(len)
