#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ..import MYDLL

NETLINK_NETFILTER = 12
nfnl = MYDLL('libnl-nf-3.so.200')
