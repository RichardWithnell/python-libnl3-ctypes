#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from . import TASKSTATS_GENL_VERSION, TASKSTATS_CMD_GET, TASKSTATS_CMD_ATTR_REGISTER_CPUMASK
from . import family_id, family_hdrsize
from .nlmsghdr import NlMsgHdr
from .util import get_all_cpus
from ..message import Message as _Message
from ..controller import CtrlCache
from ... import NL_AUTO_PORT, NL_AUTO_SEQ

class Message(_Message):
    _NlMsgHdr_class = NlMsgHdr

    def taskmsg_put(self, port, seq, flags, cmd):
        return super(Message, self).genlmsg_put(port, seq, family_id, family_hdrsize, flags, cmd, TASKSTATS_GENL_VERSION)

    def taskmsg_put_register_cpumask(self, cpumask=None):
        if cpumask is None:
            cpumask = get_all_cpus()
        self.taskmsg_put(NL_AUTO_PORT, NL_AUTO_SEQ, 0, TASKSTATS_CMD_GET)
        self.nla_put_string(TASKSTATS_CMD_ATTR_REGISTER_CPUMASK, cpumask)
