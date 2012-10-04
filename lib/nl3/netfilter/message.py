#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_uint8, c_uint16
from ...import  wrap_ptr
from ..message import Message as _Message
from .import nfnl

#noinspection PyUnusedLocal
@wrap_ptr(nfnl, c_uint8, c_uint8, c_int, c_uint8, c_uint16)
def nfnlmsg_alloc_simple(subsys_id, type, flags, family, res_id):
    """
    struct nl_msg* nfnlmsg_alloc_simple     (       uint8_t         subsys_id,
    uint8_t         type,
    int     flags,
    uint8_t         family,
    uint16_t        res_id
    )"""


class Message(_Message):
    def __init__(self, subsys_id, type, flags, family, res_id):
        ptr = nfnlmsg_alloc_simple(subsys_id, type, flags, family, res_id)
        super(Message, self).__init__(ptr)
        self._need_free = True

