#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ....ctypes.libnl3 import *
from ....ctypes.taskstats import *
from .. import resolve_family
from ..genl_msghdr import GenlMsgHdr
from ..nlmsghdr import NlMsgHdrGENL
from ..message import MessageGENL
from .util import get_all_cpus


class GenlMsgHdrTS(GenlMsgHdr):
    _family_hdrlen = None
    _family_id = None
    _version = TASKSTATS_GENL_VERSION

#TODO: if kernel have different version log this
(GenlMsgHdrTS._family_id, GenlMsgHdrTS._family_hdrlen) = resolve_family(TASKSTATS_GENL_NAME)


class NlMsgHdrTS(NlMsgHdrGENL):
    _GenlMsgHdr_class = GenlMsgHdrTS


class MessageTS(MessageGENL):
    _NlMsgHdr_class = NlMsgHdrTS

    def put_register_cpumask(self, cpumask=None):
        if cpumask is None:
            cpumask = get_all_cpus()
        self.put(NL_AUTO_PORT, NL_AUTO_SEQ, 0, TASKSTATS_CMD_GET)
        self.put_string(TASKSTATS_CMD_ATTR_REGISTER_CPUMASK, cpumask)
