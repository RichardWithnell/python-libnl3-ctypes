#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_void_p
from . import nl
from .. import StdNL, swrap

c_nl_cache_p = c_void_p

@swrap(nl, None, None, c_nl_cache_p)
def nl_cache_free():
    """     void nl_cache_free(struct nl_cache * cache) """

class NlCache(StdNL):
    _free_ptr = nl_cache_free
