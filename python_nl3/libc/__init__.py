#!/usr/bin/python
#coding: utf-8

from __future__ import absolute_import

import os
from ctypes import c_void_p, c_int, c_char_p, cdll
from ctypes.util import find_library
from .. import nullptr_check, StdNL, swrap

libc = cdll.LoadLibrary(find_library('libc'))

c_FILE_p = c_void_p

@swrap(libc, nullptr_check, c_FILE_p, c_int, c_char_p)
def fdopen(): pass

@swrap(libc, nullptr_check, c_FILE_p, c_char_p, c_char_p)
def fopen(): pass

@swrap(libc, None, None, c_FILE_p)
def fclose(): pass

def file2FILE(fileobj):
    fileobj.flush()
    # fclose will close() descriptor. so, we need to duplicate current one
    fd = os.dup(fileobj.fileno())
    try:
        return fdopen(fd, fileobj.mode)
    except:
        os.close(fd)
        raise


class FILE(StdNL):
    # TODO: error checking using errno and == EOF
    _free_ptr = fclose
    def __init__(self, item, *args):
        if item is None:
            raise ValueError('Can not create FILE* from NULL pointer')
        if isinstance(item, file):
            if args:
                raise ValueError('Extra arguments passed')
            self._alloc_ptr = lambda : file2FILE(item)
            super(FILE, self).__init__()
            return
        if isinstance(item, basestring):
            self._alloc_ptr = lambda : fopen(item, *args)
            super(FILE, self).__init__()
            return
        if isinstance(item, c_FILE_p):
            super(FILE, self).__init__(item)
            return
        raise ValueError('Unknown base pointer type')
