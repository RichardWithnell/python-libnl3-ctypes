#coding: utf-8

from __future__ import absolute_import
from ctypes import c_int, c_void_p, CFUNCTYPE, byref
from functools import wraps
from ...ctypes import MYDLL, wrap_char_ptr_no_check, common_loader, wrap_int, wrap_void, wrap_ptr
from .msg import c_nl_msg_p

nl = MYDLL('libnl-3.so.200')

#TODO: move to separate modules
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


#noinspection PyUnusedLocal
@wrap_char_ptr_no_check(nl, c_int)
def nl_geterror(errcode):
    """
    const char* nl_geterror(int err); // reconstructed.
    :type errcode: int or c_int
    :rtype : string
    """


class NetlinkException(Exception):
    """
    Any libnl3 error are subclasses of this base class
    """


def errcode_check(result, func, args):
    """
    This is python ctypes error checker used in libnl3 functions
    :type result: c_int
    :rtype : c_int
    """
    if result < 0:
        raise NetlinkException(nl_geterror(result), result, func, args)
    return result


def wrap_nl_err(*args):
    """
    Used to mark libnl3 functions tha may raise NetlinkException
    in case of error
    """
    return lambda original: common_loader(original, errcode_check, c_int, *args)


def wrap_ret_last_dbl_ptr(original):
    @wraps(original)
    def fun(*args):
        ret = c_void_p()
        new_args = args + (byref(ret),)
        original(*new_args)
        return ret

    return fun


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

