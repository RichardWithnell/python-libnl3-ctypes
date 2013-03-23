#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from .. import NLM_F_ACK, NLM_F_ROOT, NLM_F_MATCH, NLM_F_DUMP
from .message import Message
from .message import nfnlmsg_alloc_simple

# mnl.h
NFNL_SUBSYS_IPSET = 6
IPSET_CMD_LIST = 7
IPSET_PROTOCOL = 6

# Command-level attributes
IPSET_ATTR_UNSPEC = 0
IPSET_ATTR_PROTOCOL = 1    # 1: Protocol version
IPSET_ATTR_SETNAME = 2     # 2: Name of the set
IPSET_ATTR_TYPENAME = 3    # 3: Typename
IPSET_ATTR_SETNAME2 = IPSET_ATTR_TYPENAME # Setname at rename/swap
IPSET_ATTR_REVISION = 4    # 4: Settype revision
IPSET_ATTR_FAMILY = 5      # 5: Settype family
IPSET_ATTR_FLAGS = 6       # 6: Flags at command level
IPSET_ATTR_DATA = 7        # 7: Nested attributes
IPSET_ATTR_ADT = 8         # 8: Multiple data containers
IPSET_ATTR_LINENO = 9      # 9: Restore lineno
IPSET_ATTR_PROTOCOL_MIN = 10 # 10: Minimal supported version number
IPSET_ATTR_REVISION_MIN = IPSET_ATTR_PROTOCOL_MIN, # type rev min


# See mnl.c
def nfnl_ipset_msg_alloc_simple(cmd, family):
    """
    cmd: IPSET_CMD_*
    family: AF_INET=2

    build request. All request should contain IPSET_ATTR_PROTOCOL equal to IPSET_PROTOCOL.
    This function allocates only requests..
    """
    msg = Message(nfnlmsg_alloc_simple(NFNL_SUBSYS_IPSET, cmd, NLM_F_ACK|NLM_F_ROOT|NLM_F_MATCH|NLM_F_DUMP, family, 0))
    msg.nla_put_u8(IPSET_ATTR_PROTOCOL, IPSET_PROTOCOL)
    return msg

def nfnl_ipset_build_list_request(family, setname=None):
    """
    family: AF_INET=2
    """
    msg = nfnl_ipset_msg_alloc_simple(IPSET_CMD_LIST, family)
    if setname is not None:
        print dir(msg)
        msg.nla_put_string(IPSET_ATTR_SETNAME, setname)
    return msg
