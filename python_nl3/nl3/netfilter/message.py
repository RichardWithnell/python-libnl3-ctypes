#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int, c_uint8, c_uint16
from ... import swrap, nullptr_check
from .. import errcode_check, wrap
from ..message import Message as _Message
from ..message import c_nl_msg_p
from . import nfnl

@swrap(nfnl, nullptr_check, c_nl_msg_p, c_uint8, c_uint8, c_int, c_uint8, c_uint16)
def nfnlmsg_alloc_simple():
    """
struct nl_msg* nfnlmsg_alloc_simple     (       uint8_t         subsys_id,
uint8_t         type,
int     flags,
uint8_t         family,
uint16_t        res_id 
)"""


class Message(_Message):
    pass
