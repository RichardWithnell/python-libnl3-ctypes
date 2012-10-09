# coding=utf-8

from __future__ import absolute_import

from .ctypes.libc import *

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
