#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from ctypes import c_void_p, c_uint32, c_int, c_char_p, c_uint8, c_size_t, c_uint16
from .import nl, wrap_nl_err
from .nlmsghdr import NlMsgHdr
from ..import wrap_ptr, wrap_void, wrap_ptr_no_check
from ..libc import FILE

NLMSG_ALIGNTO = 4

c_nl_msg_p = c_void_p

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_msg_p)
def nlmsg_free(nlmsg):
    """ void nlmsg_get(struct nl_msg *msg) """


@wrap_ptr(nl)
def nlmsg_alloc():
    """ struct nl_msg *nlmsg_alloc(void) """

#noinspection PyUnusedLocal
@wrap_ptr(nl, c_int, c_int)
def nlmsg_alloc_simple(msgtype, flags):
    """  struct nl_msg *nlmsg_alloc_simple(int nlmsgtype, int flags) """

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_msg_p, c_void_p)
def nl_msg_dump(msg, filep):
    """ void nl_msg_dump(struct nl_msg *msg, FILE *ofd) """

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nl_msg_p)
def nlmsg_hdr(msg):
    """ struct nlmsghdr* nlmsg_hdr(struct nl_msg * n) """

#noinspection PyUnusedLocal
@wrap_ptr(nl, c_nl_msg_p, c_uint32, c_uint32, c_int, c_int, c_int)
def nlmsg_put(msg, pid, seq, type_, payload, flags):
    """struct nlmsghdr *nlmsg_put(struct nl_msg *n, uint32_t pid, uint32_t seq, int type, int payload, int flags)"""

#noinspection PyUnusedLocal
@wrap_ptr(nl, c_nl_msg_p, c_size_t, c_int)
def nlmsg_reserve(msg, len, pad):
    """void* nlmsg_reserve(struct nl_msg * n,size_t len, int pad) """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_msg_p, c_int, c_char_p)
def nla_put_string(msg, attrtype, string):
    """ int nla_put_string(struct nl_msg *msg, int attrtype, const char *str) """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint8)
def nla_put_u8(msg, attrtype, value):
    """ int nla_put_u8(struct nl_msg *msg, int attrtype, uint8_t value) """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint16)
def nla_put_u16(msg, attrtype, value):
    """ int nla_put_u16(struct nl_msg *msg, int attrtype, uint16_t value) """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint32)
def nla_put_u32(msg, attrtype, value):
    """  int nla_put_u32(struct nl_msg *msg, int attrtype, uint32_t value) """


class Message(object):
    _NlMsgHdr_class = NlMsgHdr

    def __init__(self, ptr=None, parent=None, msgtype=None, flags=None):
        self._need_free = False
        if ptr is not None:
            self._as_parameter_ = ptr
            self._parent = parent
        else:
            if msgtype is not None and flags is not None:
                self._as_parameter_ = nlmsg_alloc_simple(msgtype, flags)
            else:
                self._as_parameter_ = nlmsg_alloc()
            self._need_free = True

    def dump(self, target):
        if isinstance(target, (FILE, c_void_p)):
            return nl_msg_dump(self, target)

        if isinstance(target, (int, long)):
            with FILE(fd=target, mode='w') as fileobj:
                return nl_msg_dump(self, fileobj)

        if isinstance(target, basestring):
            with FILE(filename=target, mode='w') as fileobj:
                return nl_msg_dump(self, fileobj)

    def put(self, msg, pid, seq, type_, payload, flags):
        ptr = nlmsg_put(msg, pid, seq, type_, payload, flags)
        return self._NlMsgHdr_class(ptr=ptr, parent=self)

    def hdr(self):
        ptr = nlmsg_hdr(self)
        return self._NlMsgHdr_class(ptr=ptr, parent=self)

    reserve = lambda self, len, pad: nlmsg_reserve(self, len, pad)
    put_string = lambda self, attrtype, string: nla_put_string(self, attrtype, string)
    put_u8 = lambda self, attrtype, value: nla_put_u8(self, attrtype, value)
    put_u16 = lambda self, attrtype, value: nla_put_u16(self, attrtype, value)
    put_u32 = lambda self, attrtype, value: nla_put_u32(self, attrtype, value)


    def _free(self):
        nlmsg_free(self)
        del self._as_parameter_


    def __del__(self):
        if self._need_free:
            self._free()
            self._need_free = False
