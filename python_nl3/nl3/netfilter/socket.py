#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_int
from .. import errcode_check, wrap
from ..socket import Socket as _Socket
from ..socket import c_nl_sock_p
from . import nfnl

class Socket(_Socket):
    @wrap(nfnl, errcode_check, c_int, c_nl_sock_p)
    def nfnl_connect(): pass
