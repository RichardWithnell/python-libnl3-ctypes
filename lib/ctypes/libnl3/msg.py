# coding=utf-8

from __future__ import absolute_import
from ctypes import c_int, c_void_p, c_uint32, c_size_t
from lib.ctypes import wrap_void, wrap_ptr, wrap_ptr_no_check, wrap_int
from lib.ctypes.libnl3 import nl, c_nlmsghdr_p

NL_AUTO_PORT = 0
NL_AUTO_SEQ = 0
NL_AUTO_PID = NL_AUTO_PORT

# NLMSG_ALIGNTO = 4 # should not be here -- kernel header...
c_nl_msg_p = c_void_p


@wrap_void(nl, c_nl_msg_p)
def nlmsg_free(nlmsg):
    """ void nlmsg_get(struct nl_msg *msg) """


@wrap_ptr(nl)
def nlmsg_alloc():
    """ struct nl_msg *nlmsg_alloc(void) """


@wrap_ptr(nl, c_int, c_int)
def nlmsg_alloc_simple(msgtype, flags):
    """  struct nl_msg *nlmsg_alloc_simple(int nlmsgtype, int flags) """


@wrap_void(nl, c_nl_msg_p, c_void_p)
def nl_msg_dump(msg, filep):
    """ void nl_msg_dump(struct nl_msg *msg, FILE *ofd) """


@wrap_ptr_no_check(nl, c_nl_msg_p)
def nlmsg_hdr(msg):
    """ struct nlmsghdr* nlmsg_hdr(struct nl_msg * n) """


@wrap_ptr(nl, c_nl_msg_p, c_uint32, c_uint32, c_int, c_int, c_int)
def nlmsg_put(msg, pid, seq, type_, payload, flags):
    """struct nlmsghdr *nlmsg_put(struct nl_msg *n, uint32_t pid, uint32_t seq, int type, int payload, int flags)"""


@wrap_ptr(nl, c_nl_msg_p, c_size_t, c_int)
def nlmsg_reserve(msg, length, pad):
    """void* nlmsg_reserve(struct nl_msg * n,size_t len, int pad) """


@wrap_ptr_no_check(nl, c_nlmsghdr_p)
def nlmsg_data(nlh):
    """void * nlmsg_data (const struct nlmsghdr *nlh)"""


@wrap_ptr_no_check(nl, c_nlmsghdr_p, c_int)
def nlmsg_attrdata(nlh, hdrlen):
    """ struct nlattr *nlmsg_attrdata(const struct nlmsghdr *nlh, int hdrlen) """


@wrap_int(nl, c_nlmsghdr_p, c_int)
def nlmsg_attrlen(nlh, hdrlen):
    """ int nlmsg_attrlen(const struct nlmsghdr *nlh, int hdrlen) """