#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import
from ....ctypes.libnl3_genl import *


class Family(object):
    def __init__(self, ptr=None, parent=None):
        self._need_free = False
        if ptr is not None:
            self._as_parameter_ = ptr
            self._parent = parent
        else:
            self._as_parameter_ = genl_family_alloc()
            self._need_free = True

    def __del__(self):
        if self._need_free:
            self._free()
            self._need_free = False

    def _free(self):
        genl_family_put(self)
        del self._as_parameter_

    @property
    def hdrsize(self):
        return genl_family_get_hdrsize(self)

    @property
    def id(self):
        return genl_family_get_id(self)
