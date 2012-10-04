#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_void_p, c_uint32, c_uint
from .import genl
from ....import wrap_ptr, wrap_void, wrap_custom

c_genl_family_p = c_void_p

@wrap_ptr(genl)
def genl_family_alloc():
    """ struct genl_family* genl_family_alloc(void )"""

#noinspection PyUnusedLocal
@wrap_void(genl, c_genl_family_p)
def genl_family_put(family):
    """ void genl_family_put(struct genl_family * family) """

#noinspection PyUnusedLocal
@wrap_custom(genl, c_uint32, c_genl_family_p)
def genl_family_get_hdrsize(family):
    """ uint32_t genl_family_get_hdrsize(struct genl_family * family) """

#noinspection PyUnusedLocal
@wrap_custom(genl, c_uint, c_genl_family_p)
def genl_family_get_id(family):
    """unsigned int genl_family_get_id(struct genl_family * family)"""


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
