#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from ctypes import byref, c_void_p, c_uint32, c_int, c_uint64
from ..import  wrap_int, wrap_ptr_no_check, wrap_custom
from .import nl
#########################
c_nlattr_p = c_void_p

#noinspection PyUnusedLocal
@wrap_int(nl, c_nlattr_p, c_int)
def nla_ok(nla, remainig):
    """ int nla_ok(const struct nlattr *nla, int remaining) """

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nlattr_p, c_nlattr_p)
def nla_next(nla, remainig):
    """  struct nlattr *nla_next(const struct nlattr *nla, int *remaining) """

#    return Attribute(result, self.msghdr_ptr)

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nlattr_p)
def nla_data(nla):
    """void* nla_data(const struct nlattr * nla)"""

#noinspection PyUnusedLocal
@wrap_int(nl, c_nlattr_p)
def nla_type(nla):
    """int nla_type(const struct nlattr * nla)"""

#noinspection PyUnusedLocal
@wrap_int(nl, c_nlattr_p)
def nla_len(nla):
    """int nla_len(const struct nlattr * nla)"""

#noinspection PyUnusedLocal
@wrap_custom(nl, c_uint32, c_nlattr_p)
def nla_get_u32(nla):
    """ uint32_t nla_get_u32(struct nlattr * nla) """

#noinspection PyUnusedLocal
@wrap_custom(nl, c_uint64, c_nlattr_p)
def nla_get_u64(nla):
    """ uint64_t nla_get_u64(struct nlattr * nla) """


class Attribute(object):
    def __init__(self, ptr=None, parent=None):
        self._parent = parent
        self._as_parameter_ = ptr

    ok = lambda self, len: bool(nla_ok(self, len))
    data = lambda self: nla_data(self)
    len = lambda self: nla_len(self)
    type = lambda self: nla_type(self)
    get_u32 = lambda self: nla_get_u32(self)
    get_u64 = lambda self: nla_get_u64(self)

    def next(self, remainig):
        rem = c_int(remainig)
        # never return NULL
        x = nla_next(self, byref(rem))
        return (Attribute(ptr=x, parent=self._parent), rem)

    ########### custom  functions
    def nested_attr(self):
        return

    def attributes(self):
        attr = Attribute(ptr=self.data(), parent=self._parent)
        len = self.len()
        while attr.ok(len):
            yield attr
            (attr, len) = attr.next(len)
