#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from .. import NLM_F_ACK, NLM_F_ROOT, NLM_F_MATCH, NLM_F_DUMP
from .message import Message, nfnlmsg_alloc_simple

# mnl.h
NFNL_SUBSYS_IPSET = 6
IPSET_CMD_LIST = 7
IPSET_PROTOCOL = 6
IPSET_ATTR_PROTOCOL = 1

# See mnl.c
def nfnl_ipset_msg_alloc_simple(cmd, family):
    """
    cmd: IPSET_CMD_*
    family: AF_INET=2
    """
    return Message(nfnlmsg_alloc_simple(NFNL_SUBSYS_IPSET, cmd, NLM_F_ACK|NLM_F_ROOT|NLM_F_MATCH|NLM_F_DUMP, family, 0))

def nfnl_ipset_build_list_request(family):
    """
    family: AF_INET=2
    """
    msg = nfnl_ipset_msg_alloc_simple(IPSET_CMD_LIST, family)
    msg.nla_put_u8(IPSET_ATTR_PROTOCOL, IPSET_PROTOCOL)
    return msg
