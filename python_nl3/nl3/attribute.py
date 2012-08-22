#!/usr/bin/env python
# coding: utf-8

#TODO:
# c_int  vs c_bool
# c_bool vs Exception

from __future__ import absolute_import

from ctypes import byref, c_void_p, c_uint32, c_int, c_uint64, c_bool
from .. import nullptr_check
from . import nl, wrap, fwrap
#########################
c_nlattr_p = c_void_p

class Attribute(object):
    def __init__(self, ptr, msghdr_ptr):
        self.msghdr_ptr = msghdr_ptr # prevent from MsgHdr garbage collection
        self._as_parameter_ = ptr

    # return c_int in original
    @wrap(nl, None, c_bool, c_nlattr_p, c_int)
    def nla_ok(): pass

    @fwrap(nl, nullptr_check, c_nlattr_p, c_nlattr_p)
    def nla_next(self, result):
        return Attribute(result, self.msghdr_ptr)

    @wrap(nl, nullptr_check, c_void_p, c_nlattr_p)
    def nla_data():
        """void* nla_data(const struct nlattr * nla)"""

    @wrap(nl, None, c_int, c_nlattr_p)
    def nla_type():
        """int nla_type(const struct nlattr * nla)"""

    @wrap(nl, None, c_int, c_nlattr_p)
    def nla_len():
        """int nla_len(const struct nlattr * nla)"""

    @wrap(nl, None, c_uint32, c_nlattr_p)
    def nla_get_u32():
        """ uint32_t nla_get_u32(struct nlattr * nla) """

    @wrap(nl, None, c_uint64, c_nlattr_p)
    def nla_get_u64():
        """ uint64_t nla_get_u64(struct nlattr * nla) """

    ########### custom  functions
    def nested_attr(self):
        return Attribute(self.nla_data(), self.msghdr_ptr)

    def attributes(self):
        pos = self.nested_attr()
        rem = c_int(self.nla_len())
        while pos.nla_ok(rem):
            yield pos
            pos = pos.nla_next(byref(rem))
