#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

import os
from ctypes import c_void_p, c_int, c_char_p, get_errno
from . import common_loader, MYDLL

libc = MYDLL('libc.so.6', use_errno=True)

c_FILE_p = c_void_p


#noinspection PyUnusedLocal
def errno_check(result, func, args):
    """
    :rtype : int
    :type result: int
    """
    if result == -1:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))
    return result


#noinspection PyUnusedLocal
def ptr_errno_check(result, func, args):
    if result == 0:
        errno = get_errno()
        raise OSError(errno, os.strerror(errno))
    return result


def wrap_errno(*args):
    """
    Decorator, that checks if retun value is -1,
    and raises error in that case
    """
    return lambda original: common_loader(original, errno_check, c_int, *args)


def wrap_ptr_errno(*args):
    """
    Decorator, that checks if return value (pointer) is zero,
    and raises error in that case
    """
    return lambda original: common_loader(original, ptr_errno_check, c_void_p, *args)

#noinspection PyUnusedLocal
@wrap_errno(libc, c_FILE_p)
def fclose(file_p):
    """ int fclose(FILE *fp); """

#noinspection PyUnusedLocal
@wrap_ptr_errno(libc, c_int, c_char_p)
def fdopen(fd, mode):
    """ FILE *fdopen(int fd, const char *mode); """

#noinspection PyUnusedLocal
@wrap_ptr_errno(libc, c_char_p, c_char_p)
def fopen(path, mode):
    """ FILE *fopen(const char *path, const char *mode); """
