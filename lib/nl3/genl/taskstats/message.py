#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ....ctypes.libnl3 import *
from ....ctypes.taskstats import *
from ..message import Message as _Message
from ..ctrl.controller import CtrlCache
from .util import get_all_cpus


def _resolve_family():
    family = CtrlCache().search_by_name(TASKSTATS_GENL_NAME)
    return (family.id, family.hdrsize)

(family_id, family_hdrsize) = _resolve_family()

class Message(_Message):
    #noinspection PyMethodOverriding
    def put(self, port, seq, flags, cmd):
        return super(Message, self).put(port, seq, family_id, family_hdrsize, flags, cmd, TASKSTATS_GENL_VERSION)

    def put_register_cpumask(self, cpumask=None):
        if cpumask is None:
            cpumask = get_all_cpus()
        self.put(NL_AUTO_PORT, NL_AUTO_SEQ, 0, TASKSTATS_CMD_GET)
        self.put_string(TASKSTATS_CMD_ATTR_REGISTER_CPUMASK, cpumask)
