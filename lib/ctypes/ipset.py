#!/usr/bin/python
#coding: utf-8
from __future__ import absolute_import

from .libnl3 import *

# mnl.h
NFNL_SUBSYS_IPSET = 6
IPSET_CMD_LIST = 7
IPSET_PROTOCOL = 6
IPSET_ATTR_PROTOCOL = 1

AF_INET = 2

# See mnl.c
IPSET_FLAGS = {
    IPSET_CMD_LIST: NLM_F_ACK | NLM_F_ROOT | NLM_F_MATCH | NLM_F_DUMP,
}
