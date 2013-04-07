# coding=utf-8

from __future__ import absolute_import

from ctypes import c_int, c_uint8, c_uint16, c_uint32, c_uint64, c_void_p, c_char_p
from functools import wraps
from ...ctypes import wrap_int, wrap_ptr_no_check, wrap_custom
from . import nl, wrap_nl_err, c_nl_msg_p

c_nlattr_p = c_void_p


def wrap_nla_next(original):
    @wraps(original)
    def fun(nla, remainig):
        """
        :rtype : (c_nlattr_p, int)
        :type nla: c_nlattr_p
        :type remainig: int
        """
        rem = c_int(remainig)
        _next = original(nla, rem)
        return (_next, rem.value)

    return fun


@wrap_nla_next
@wrap_ptr_no_check(nl, c_nlattr_p, c_nlattr_p)
def nla_next(nla, remainig):
    """
    struct nlattr *nla_next(const struct nlattr *nla, int *remaining)
    :type nla: c_nlattr_p
    :type remainig: int
    :rtype : (c_nlattr_p, int)
    """


@wrap_int(nl, c_nlattr_p, c_int)
def nla_ok(nla, remainig):
    """
    int nla_ok(const struct nlattr *nla, int remaining)
    :rtype : int
    :type nla: c_nlattr_p
    :type remainig: int
    """


@wrap_ptr_no_check(nl, c_nlattr_p)
def nla_data(nla):
    """
    void* nla_data(const struct nlattr * nla)
    :rtype : c_void_p
    :type nla: c_nlattr_p
    """


@wrap_int(nl, c_nlattr_p)
def nla_type(nla):
    """
    int nla_type(const struct nlattr * nla)
    :type nla: c_nlattr_p
    :rtype: int
    """


@wrap_int(nl, c_nlattr_p)
def nla_len(nla):
    """
    int nla_len(const struct nlattr * nla)
    :type nla: c_nlattr_p
    :rtype: int
    """


@wrap_custom(nl, c_uint8, c_nlattr_p)
def nla_get_u8(nla):
    """
    uint8_t nla_get_u8(struct nlattr * nla)
    :type nla: c_nlattr_p
    :rtype: int
    """


@wrap_custom(nl, c_uint16, c_nlattr_p)
def nla_get_u16(nla):
    """
    uint16_t nla_get_u16(struct nlattr * nla)
    :type nla: c_nlattr_p
    :rtype: int
    """


@wrap_custom(nl, c_uint32, c_nlattr_p)
def nla_get_u32(nla):
    """
    uint32_t nla_get_u32(struct nlattr * nla)
    :type nla: c_nlattr_p
    :rtype: int
    """


@wrap_custom(nl, c_uint64, c_nlattr_p)
def nla_get_u64(nla):
    """
    uint64_t nla_get_u64(struct nlattr * nla)
    :type nla: c_nlattr_p
    :rtype: int
    """


@wrap_nl_err(nl, c_nl_msg_p, c_int, c_char_p)
def nla_put_string(msg, attrtype, string):
    """ int nla_put_string(struct nl_msg *msg, int attrtype, const char *str) """


@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint8)
def nla_put_u8(msg, attrtype, value):
    """ int nla_put_u8(struct nl_msg *msg, int attrtype, uint8_t value) """


@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint16)
def nla_put_u16(msg, attrtype, value):
    """ int nla_put_u16(struct nl_msg *msg, int attrtype, uint16_t value) """


@wrap_nl_err(nl, c_nl_msg_p, c_int, c_uint32)
def nla_put_u32(msg, attrtype, value):
    """  int nla_put_u32(struct nl_msg *msg, int attrtype, uint32_t value) """