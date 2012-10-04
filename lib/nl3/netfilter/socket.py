#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import  c_void_p
from ..import  wrap_nl_err
from ..socket import Socket as _Socket
from .import nfnl

c_nl_sock_p = c_void_p

#noinspection PyUnusedLocal
@wrap_nl_err(nfnl, c_nl_sock_p)
def nfnl_connect(sock):
    """ int nfnl_connect(struct nl_sock *sk) """


class Socket(_Socket):
    connect = lambda self: nfnl_connect(self)
