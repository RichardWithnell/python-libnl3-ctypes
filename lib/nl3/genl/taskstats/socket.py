#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from .message import Message
from ..socket import Socket as Socket_

class Socket(Socket_):
    _message_class = Message

    def register_cpumask(self, cpumask=None):
        msg = self._message_class()
        msg.put_register_cpumask(cpumask)

        self.send_auto_complete(msg)
        self.wait_for_ack()
        # http://www.infradead.org/~tgr/libnl/doc/core.html#core_sk_seq_num
        self.disable_seq_check()