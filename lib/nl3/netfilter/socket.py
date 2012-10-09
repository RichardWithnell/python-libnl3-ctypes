#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ...ctypes.libnl3_nf import nfnl_connect
from ..socket import Socket as _Socket


class Socket(_Socket):
    connect = lambda self: nfnl_connect(self)
