#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import cdll
from ctypes.util import find_library

NETLINK_NETFILTER = 12
nfnl = cdll.LoadLibrary(find_library('nl-nf-3'))
