#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from lib.ctypes.libnl3.attr import nla_ok, nla_next, nla_data, nla_type, nla_len, nla_get_u8, nla_get_u16, nla_get_u32, nla_get_u64


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
    len_ = lambda self: nla_len(self)
    type_ = lambda self: nla_type(self)

    _u8 = property(nla_get_u8)
    _u16 = property(nla_get_u16)
    _u32 = property(nla_get_u32)
    _u64 = property(nla_get_u64)

    @property
    def value(self):
        """
        Python-only function. You should use only this function
        instead of properties like ._u8  or ._u64

        This is not as fast as in C, but less error prone
        """
        mytype = self.type_()

        if mytype == NLA_U8:
            return self._u8
        if mytype == NLA_U16:
            return self._u16
        if mytype == NLA_U32:
            return self._u32
        if mytype == NLA_U64:
            return self._u64
        raise NotImplementedError('Unknown my type', mytype)

    def next(self, remainig):
        """
        Returns next attribute in the chain of attributes
        :rtype : (Attribute, int)
        :type remainig: int

        """
        # never return NULL
        (attr, remainig) = nla_next(self, remainig)
        return (Attribute(ptr=attr, parent=self._parent), remainig)

    def __iter__(self):
        """ Yields enclosed attributes """
        # Sanity check - slower than same in C ...
        if self.type_ != NLA_NESTED:
            raise RuntimeError('Trying to iterate enclosed attributes of non-nested attribute')

        attr = Attribute(ptr=self.data(), parent=self)
        _len = self.len_()
        while attr.ok(_len):
            yield attr
            (attr, _len) = attr.next(_len)
        if _len:
            raise RuntimeError('Extra data after last enclosed attribute')
        raise StopIteration()
