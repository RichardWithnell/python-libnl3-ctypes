#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from ..import MYDLL, wrap_char_ptr_no_check, common_loader
from ctypes import c_int

nl = MYDLL('libnl-3.so.200')

#TODO: move to separate modules
NL_AUTO_PORT = 0
NL_AUTO_SEQ = 0

NLM_F_REQUEST = 1
NLM_F_MULTI = 2
NLM_F_ACK = 4
NLM_F_ECHO = 8
NLM_F_ROOT = 0x100
NLM_F_MATCH = 0x200
NLM_F_ATOMIC = 0x400
NLM_F_DUMP = NLM_F_ROOT | NLM_F_MATCH
NLM_F_REPLACE = 0x100
NLM_F_EXCL = 0x200
NLM_F_CREATE = 0x400
NLM_F_APPEND = 0x800

#noinspection PyUnusedLocal
@wrap_char_ptr_no_check(nl, c_int)
def nl_geterror(errcode):
    """ const char* nl_geterror(int err); // reconstructed."""


class NetlinkException(Exception):
    pass


def errcode_check(result, func, args):
    if result < 0:
        raise NetlinkException(nl_geterror(result), result, func, args)
    return result


def wrap_nl_err(*args):
    return lambda original: common_loader(original, errcode_check, c_int, *args)
