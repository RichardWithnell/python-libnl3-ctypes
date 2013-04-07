#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from lib.ctypes.libnl3.attr import nla_put_string, nla_put_u8, nla_put_u16, nla_put_u32
from lib.ctypes.libnl3.msg import nlmsg_free, nlmsg_alloc, nlmsg_alloc_simple, nl_msg_dump, nlmsg_hdr, nlmsg_put, nlmsg_reserve
from ..libc import FILE
from .nlmsghdr import NlMsgHdr
from contextlib import closing

class Message(object):
    _NlMsgHdr_class = NlMsgHdr

    def __init__(self, ptr=None, parent=None, msgtype=None, flags=0):
        self._need_free = False
        if ptr is not None:
            self._as_parameter_ = ptr
            self._parent = parent
        else:
            if msgtype is not None:
                self._as_parameter_ = nlmsg_alloc_simple(msgtype, flags)
            else:
                self._as_parameter_ = nlmsg_alloc()
            self._need_free = True

    def dump(self, target):
        if isinstance(target, FILE):
            return nl_msg_dump(self, target)

        if isinstance(target, (int, long)):
            with closing(FILE(fd=target, mode='w')) as fileobj:
                return nl_msg_dump(self, fileobj)

        if isinstance(target, basestring):
            with closing(FILE(filename=target, mode='w')) as fileobj:
                return nl_msg_dump(self, fileobj)

    def put(self, msg, pid, seq, type_, payload, flags):
        ptr = nlmsg_put(msg, pid, seq, type_, payload, flags)
        return self._NlMsgHdr_class(ptr=ptr, parent=self)

    def hdr(self):
        ptr = nlmsg_hdr(self)
        return self._NlMsgHdr_class(ptr=ptr, parent=self)

    reserve = lambda self, _len, pad: nlmsg_reserve(self, _len, pad)
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
