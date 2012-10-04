# coding: utf-8

#noinspection PyUnusedLocal
from ctypes import c_void_p, c_char_p
from ...import wrap_nl_err
from ..import genl

c_nl_sock_p = c_void_p

#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p, c_char_p)
def genl_ctrl_resolve(sock, name):
    """int genl_ctrl_resolve(struct nl_sock *, const char *); """

#noinspection PyUnusedLocal
@wrap_nl_err(genl, c_nl_sock_p, c_char_p, c_char_p)
def genl_ctrl_resolve_grp(sock, family, grp):
    """int genl_ctrl_resolve_grp(struct nl_sock *sk, const char *family, const char *grp); """


