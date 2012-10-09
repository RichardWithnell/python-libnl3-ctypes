#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import c_void_p, c_char_p, c_int, POINTER, c_uint32, c_uint, c_uint8
from .import MYDLL, wrap_ptr, wrap_void, wrap_custom, wrap_ptr_no_check, wrap_int
from .libnl3 import wrap_nl_err, nlmsg_data

NETLINK_GENERIC = 16

genl = MYDLL('libnl-genl-3.so.200')

c_nl_sock_p = c_void_p
c_nl_cache_p = c_void_p
c_nl_msg_p = c_void_p
c_nlmsghdr_p = c_void_p

c_genl_family_p = c_void_p
c_genlmsghdr_p = c_void_p



##############################################################
#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p, c_char_p)
def genl_ctrl_resolve(sock, name):
    """int genl_ctrl_resolve(struct nl_sock *, const char *); """

#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p, c_char_p, c_char_p)
def genl_ctrl_resolve_grp(sock, family, grp):
    """int genl_ctrl_resolve_grp(struct nl_sock *sk, const char *family, const char *grp); """

#############################################################

#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p, POINTER(c_nl_cache_p))
def genl_ctrl_alloc_cache(sock, presult):
    """ int genl_ctrl_alloc_cache(struct nl_sock *sk, struct nl_cache **result) """

#noinspection PyUnusedLocal
@wrap_ptr(genl, c_nl_cache_p, c_int)
def genl_ctrl_search(cache, id):
    """ struct genl_family *genl_ctrl_search(struct nl_cache *, int id); """

#noinspection PyUnusedLocal
@wrap_ptr(genl, c_nl_cache_p, c_char_p)
def genl_ctrl_search_by_name(cache, name):
    """  struct genl_family *genl_ctrl_search_by_name(struct nl_cache *cache, const char *name) """

###############################################################################################


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

####################################################################################


#noinspection PyUnusedLocal
@wrap_ptr_no_check(genl, c_genlmsghdr_p, c_int)
def genlmsg_attrdata(gnlh, hdrlen):
    """ struct nlattr* genlmsg_attrdata(const struct genlmsghdr * gnlh, int hdrlen)"""

#noinspection PyUnusedLocal
@wrap_int(genl, c_genlmsghdr_p, c_int)
def genlmsg_attrlen(gnlh, hdrlen):
    """int genlmsg_attrlen(const struct genlmsghdr * gnlh, int hdrlen)"""

#noinspection PyUnusedLocal
@wrap_ptr_no_check(genl, c_genlmsghdr_p)
def genlmsg_data(gnlh):
    """void* genlmsg_data(const struct genlmsghdr * gnlh)"""

####################################################################

#noinspection PyUnusedLocal
@wrap_ptr(genl, c_nl_msg_p, c_uint32, c_uint32, c_int, c_int, c_int, c_uint8, c_uint8)
def genlmsg_put(msg, port, seq, family, hdrlen, flags, cmd, version):
    """ void *genlmsg_put(struct nl_msg *msg, uint32_t port, uint32_t seq, int family, int hdrlen, int flags, uint8_t cmd, uint8_t version) """

##################################################

#noinspection PyUnusedLocal
@wrap_int(genl, c_nlmsghdr_p, c_int)
def genlmsg_valid_hdr(nlh, hdrlen):
    """int genlmsg_valid_hdr(struct nlmsghdr * nlh, int hdrlen)"""

try:
    #noinspection PyUnusedLocal
    @wrap_ptr_no_check(genl, c_genlmsghdr_p)
    def genlmsg_hdr(nlh):
        """ struct genlmsghdr* genlmsg_hdr(struct nlmsghdr * nlh) """

except AttributeError:
    #noinspection PyRedeclaration
    def genlmsg_hdr(nlh):
        return nlmsg_data(nlh)

########################################################

#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p)
def genl_connect(sock):
    """ int genl_connect(struct nl_sock *sk) """

#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p, c_int, c_int, c_int, c_int)
def genl_send_simple(sock, family, cmd, version, flags):
    """ int genl_send_simple(struct nl_sock *sk, int family, int cmd, int version, int flags) """
