#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import
from ctypes import c_int, c_void_p, c_uint32, c_uint64, CFUNCTYPE, c_size_t, c_uint8, c_uint16, POINTER, byref
from functools import wraps

from . import *


nl = MYDLL('libnl-3.so.200')

#TODO: move to separate modules
NL_AUTO_PORT = 0
NL_AUTO_SEQ = 0
NL_AUTO_PROVIDE = 1
NL_CB_VALID = 0
NL_CB_CUSTOM = 3
NL_CB_MSG_IN = 5
NL_OK = 0
NL_STOP = 2
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

c_nl_cache_mngr_p = c_void_p
c_nl_object_p = c_void_p
c_nl_cache_p = c_void_p
c_nl_sock_p = c_void_p

c_nlmsghdr_p = c_void_p
c_nlattr_p = c_void_p

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


def wrap_ret_last_dbl_ptr(original):
    @wraps(original)
    def fun(*args):
        ret = c_void_p()
        new_args = args + (byref(ret),)
        original(*new_args)
        return ret

    return fun

#############################################################################

#noinspection PyUnusedLocal
@wrap_int(nl, c_nlattr_p, c_int)
def nla_ok(nla, remainig):
    """ int nla_ok(const struct nlattr *nla, int remaining) """


def wrap_nla_next(original):
    @wraps(original)
    def fun(nla, remainig):
        rem = c_int(remainig)
        next = original(nla, rem)
        return (next, rem.value)

    return fun

#noinspection PyUnusedLocal
@wrap_nla_next
@wrap_ptr_no_check(nl, c_nlattr_p, c_nlattr_p)
def nla_next(nla, remainig):
    """  struct nlattr *nla_next(const struct nlattr *nla, int *remaining) """

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nlattr_p)
def nla_data(nla):
    """void* nla_data(const struct nlattr * nla)"""

#noinspection PyUnusedLocal
@wrap_int(nl, c_nlattr_p)
def nla_type(nla):
    """int nla_type(const struct nlattr * nla)"""

#noinspection PyUnusedLocal
@wrap_int(nl, c_nlattr_p)
def nla_len(nla):
    """int nla_len(const struct nlattr * nla)"""

#noinspection PyUnusedLocal
@wrap_custom(nl, c_uint32, c_nlattr_p)
def nla_get_u32(nla):
    """ uint32_t nla_get_u32(struct nlattr * nla) """

#noinspection PyUnusedLocal
@wrap_custom(nl, c_uint64, c_nlattr_p)
def nla_get_u64(nla):
    """ uint64_t nla_get_u64(struct nlattr * nla) """

####################################################################################

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_cache_p)
def nl_cache_free(cache):
    """     void nl_cache_free(struct nl_cache * cache) """

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nl_cache_p)
def nl_cache_get_first(cache):
    """ struct nl_object *nl_cache_get_first(struct nl_cache *cache) """

######################################################################################

#noinspection PyUnusedLocal
@wrap_ret_last_dbl_ptr
@wrap_nl_err(nl, c_nl_sock_p, c_int, c_int, POINTER(c_nl_cache_mngr_p))
def nl_cache_mngr_alloc(sock, protocol, flags):
    """
    int nl_cache_mngr_alloc(struct nl_sock * sk,
    int protocol,
    int flags,
    struct nl_cache_mngr ** result
    )"""

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_cache_mngr_p)
def nl_cache_mngr_free(mngr):
    """void nl_cache_mngr_free(struct nl_cache_mngr * mngr)"""

# typedef void (*change_func_t)(struct nl_cache *, struct nl_object *, int, void *);
change_func_t = CFUNCTYPE(None, c_nl_cache_p, c_nl_object_p, c_void_p)

#noinspection PyUnusedLocal
@wrap_ret_last_dbl_ptr
@wrap_nl_err(nl, c_nl_cache_mngr_p, c_char_p, change_func_t, c_void_p, POINTER(c_nl_cache_p))
def nl_cache_mngr_add(mngr, name, callback, data):
    """int nl_cache_mngr_add(struct nl_cache_mngr * mngr,
    const char * name,
    change_func_t cb,
    void * data,
    struct nl_cache ** result
    )"""

######################################################################################

NLMSG_ALIGNTO = 4

c_nl_msg_p = c_void_p

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_msg_p)
def nlmsg_free(nlmsg):
    """ void nlmsg_get(struct nl_msg *msg) """


@wrap_ptr(nl)
def nlmsg_alloc():
    """ struct nl_msg *nlmsg_alloc(void) """

#noinspection PyUnusedLocal
@wrap_ptr(nl, c_int, c_int)
def nlmsg_alloc_simple(msgtype, flags):
    """  struct nl_msg *nlmsg_alloc_simple(int nlmsgtype, int flags) """

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_msg_p, c_void_p)
def nl_msg_dump(msg, filep):
    """ void nl_msg_dump(struct nl_msg *msg, FILE *ofd) """

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nl_msg_p)
def nlmsg_hdr(msg):
    """ struct nlmsghdr* nlmsg_hdr(struct nl_msg * n) """

#noinspection PyUnusedLocal
@wrap_ptr(nl, c_nl_msg_p, c_uint32, c_uint32, c_int, c_int, c_int)
def nlmsg_put(msg, pid, seq, type_, payload, flags):
    """struct nlmsghdr *nlmsg_put(struct nl_msg *n, uint32_t pid, uint32_t seq, int type, int payload, int flags)"""

#noinspection PyUnusedLocal
@wrap_ptr(nl, c_nl_msg_p, c_size_t, c_int)
def nlmsg_reserve(msg, len, pad):
    """void* nlmsg_reserve(struct nl_msg * n,size_t len, int pad) """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_msg_p, c_int, c_char_p)
def nla_put_string(msg, attrtype, string):
    """ int nla_put_string(struct nl_msg *msg, int attrtype, const char *str) """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint8)
def nla_put_u8(msg, attrtype, value):
    """ int nla_put_u8(struct nl_msg *msg, int attrtype, uint8_t value) """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint16)
def nla_put_u16(msg, attrtype, value):
    """ int nla_put_u16(struct nl_msg *msg, int attrtype, uint16_t value) """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint32)
def nla_put_u32(msg, attrtype, value):
    """  int nla_put_u32(struct nl_msg *msg, int attrtype, uint32_t value) """

#################################################################

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nlmsghdr_p)
def nlmsg_data(nlh):
    """void * nlmsg_data (const struct nlmsghdr *nlh)"""

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nlmsghdr_p, c_int)
def nlmsg_attrdata(nlh, hdrlen):
    """ struct nlattr *nlmsg_attrdata(const struct nlmsghdr *nlh, int hdrlen) """

#noinspection PyUnusedLocal
@wrap_int(nl, c_nlmsghdr_p, c_int)
def nlmsg_attrlen(nlh, hdrlen):
    """ int nlmsg_attrlen(const struct nlmsghdr *nlh, int hdrlen) """

#################################################################

#noinspection PyUnusedLocal
@wrap_ptr_no_check(nl, c_nl_object_p)
def nl_cache_get_next(obj):
    """ struct nl_object *nl_cache_get_next(struct nl_object *obj) """

#################################################################

#noinspection PyUnusedLocal
@wrap_ptr(nl)
def nl_socket_alloc():
    """ struct nl_sock *nl_socket_alloc(void) """

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_sock_p)
def nl_socket_free(sock):
    """  void nl_socket_free(struct nl_sock *sk) """


nl_recvmsg_msg_cb_t = CFUNCTYPE(c_int, c_nl_msg_p, c_void_p)

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_sock_p, c_int, c_int, c_void_p, c_void_p)
def nl_socket_modify_cb(sk, type_, kind, func, arg):
    """
    int nl_socket_modify_cb(struct nl_sock * sk,
    enum nl_cb_type type,
    enum nl_cb_kind kind,
    nl_recvmsg_msg_cb_t func,
    void * arg
    )
    """

#noinspection PyUnusedLocal
@wrap_int(nl, c_nl_sock_p)
def nl_socket_get_fd(sock):
    """ int nl_socket_get_fd(const struct nl_sock *sk) """


#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_sock_p, c_nl_msg_p)
def nl_send_auto_complete(sock, msg):
    """ """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_sock_p)
def nl_recvmsgs_default(sock):
    """ """

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_sock_p)
def nl_socket_disable_seq_check(sock):
    """ """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_sock_p)
def nl_socket_set_nonblocking(sock):
    """ """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_sock_p)
def nl_wait_for_ack(sock):
    """ """

#noinspection PyUnusedLocal
@wrap_void(nl, c_nl_sock_p)
def nl_close(sock):
    """ Just close file descriptor, not free memory """

#noinspection PyUnusedLocal
@wrap_nl_err(nl, c_nl_sock_p, c_int)
def nl_connect(sock, protocol):
    """ int nl_connect(struct nl_sock * sk, int protocol) """

#################################################################

