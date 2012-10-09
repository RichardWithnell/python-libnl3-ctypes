#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ..socket import Socket as Socket_
from .message import MessageTS

class Socket(Socket_):
    _message_class = MessageTS

    def register_cpumask(self, cpumask=None):
        msg = self._message_class()
        msg.put_register_cpumask(cpumask)

        self.send_auto_complete(msg)
        self.wait_for_ack()
        # http://www.infradead.org/~tgr/libnl/doc/core.html#core_sk_seq_num
        self.disable_seq_check()





