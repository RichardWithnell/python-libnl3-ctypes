#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ...ctypes.libnl3_nf import nfnlmsg_alloc_simple
from ..message import Message as _Message

class Message(_Message):
    def __init__(self, subsys_id, type, flags, family, res_id):
        ptr = nfnlmsg_alloc_simple(subsys_id, type, flags, family, res_id)
        super(Message, self).__init__(ptr)
        self._need_free = True

