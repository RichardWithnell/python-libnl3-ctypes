#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import
from _ctypes import get_errno

import os
from ctypes import c_void_p, c_int, c_char_p
from ..import common_loader, MYDLL

libc = MYDLL('libc.so.6', use_errno=True)

c_FILE_p = c_void_p

#noinspection PyUnusedLocal
def errno_check(result, func, args):
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
    return lambda original: common_loader(original, errno_check, c_int, *args)


def wrap_ptr_errno(*args):
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

# TODO: error checking using errno and == EOF
class FILE(object):
    def __init__(self, fd=None, ptr=None, filename=None, mode='r'):
        self._need_close = False
        if ptr is not None:
            self._as_parameter = ptr
            return
        if fd is not None:
            self._as_parameter = fdopen(fd, mode)
            self._need_close = True
            return
        if filename is not None:
            self._as_parameter = fopen(filename, mode)
            self._need_close = True
            return
        raise NotImplementedError('do not know how to create FILE object')

    def __enter__(self):
        if not self._need_close:
            raise RuntimeError('You should not ise "with" statement with file opened by pointer')
        return self

    #noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        fclose(self)
        del self._as_parameter
        self._need_close = False

    def __del__(self):
        if self._need_close:
            self.close()
