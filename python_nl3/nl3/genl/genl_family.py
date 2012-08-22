#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_void_p, c_uint32, c_uint
from ... import StdNL, swrap, nullptr_check
from .. import wrap
from . import genl

############################
c_genl_family_p = c_void_p

@swrap(genl, nullptr_check, c_genl_family_p)
def genl_family_alloc():
    """ struct genl_family* genl_family_alloc(void )"""

@swrap(genl, None, None, c_genl_family_p)
def genl_family_put():
    """ genl_family_put(struct genl_family * family) """

class Family(StdNL):
    _alloc_ptr = genl_family_alloc
    _free_ptr = genl_family_put

    def __init__(self, ptr, cache):
        self.cache = cache # prevent grabage collection
        super(Family, self).__init__(ptr)

    @wrap(genl, None, c_uint32, c_genl_family_p)
    def genl_family_get_hdrsize():
        """ uint32_t genl_family_get_hdrsize(struct genl_family * family) """

    @wrap(genl, None, c_uint, c_genl_family_p)
    def genl_family_get_id():
        """unsigned int genl_family_get_id(struct genl_family * family)"""

    @property
    def id_(self):
        return self.genl_family_get_id()

    @property
    def hdrsize(self):
        return self.genl_family_get_hdrsize()

