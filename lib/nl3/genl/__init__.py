#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from lib import MYDLL

NETLINK_GENERIC = 16
genl = MYDLL('libnl-genl-3.so.200')
