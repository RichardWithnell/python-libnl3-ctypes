#!/usr/bin/env python
# coding: utf-8

#TODO:
# c_int  vs c_bool
# c_bool vs Exception

from __future__ import absolute_import

from ctypes import c_void_p, c_uint32, c_int, c_char_p, c_uint8, c_size_t
from . import nl, wrap, errcode_check, fwrap
from .. import nullptr_check, StdNL, swrap
from ..libc import c_FILE_p
from .nlmsghdr import c_nlmsghdr_p, NlMsgHdr

NLMSG_ALIGNTO = 4

c_nl_msg_p = c_void_p # c_nl_msg_p = ctypes.POINTER(Message)
#TODO: make Message subclass of the c_void_p and so on, so eliminate ALL c_void_p in _register_* args

@swrap(nl, None, None, c_nl_msg_p)
def nlmsg_free(): pass

@swrap(nl, nullptr_check, c_nl_msg_p)
def nlmsg_alloc(): pass

@swrap(nl, nullptr_check, c_nl_msg_p, c_int, c_int)
def nlmsg_alloc_simple():
    """
    struct nl_msg* nlmsg_alloc_simple(int nlmsgtype,
    int flags
    )"""

class Message(StdNL):
    _alloc_ptr = nlmsg_alloc
    _free_ptr = nlmsg_free
    _NlMsgHdr_class = NlMsgHdr

    @wrap(nl, None, None, c_nl_msg_p, c_FILE_p)
    def nl_msg_dump (): pass

    @wrap(nl, errcode_check, c_int, c_nl_msg_p, c_int, c_char_p)
    def nla_put_string(): pass

    @wrap(nl, errcode_check, c_int, c_nl_msg_p, c_int, c_uint32)
    def nla_put_u32(): pass

    @wrap(nl, errcode_check, c_int, c_nl_msg_p, c_int, c_uint8)
    def nla_put_u8(): pass

    @fwrap(nl, nullptr_check, c_nlmsghdr_p, c_nl_msg_p)
    def nlmsg_hdr(self, result):
        """ struct nlmsghdr* nlmsg_hdr(struct nl_msg * n) """
        return self._NlMsgHdr_class(result, self)

    @fwrap(nl, nullptr_check, c_nlmsghdr_p, c_nl_msg_p, c_uint32, c_uint32, c_int, c_int, c_int)
    def nlmsg_put(self, result):
        """struct nlmsghdr *nlmsg_put(struct nl_msg *n, uint32_t pid, uint32_t seq,
                           int type, int payload, int flags)"""
        return self._NlMsgHdr_class(result, self)

    @wrap(nl, nullptr_check, c_void_p, c_nl_msg_p, c_size_t, c_int)
    def nlmsg_reserve():
        """void* nlmsg_reserve(struct nl_msg * n,size_t len,int pad )"""
