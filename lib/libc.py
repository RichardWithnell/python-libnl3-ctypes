# coding=utf-8

from __future__ import absolute_import

from .ctypes import libc as _libc, c_void_p

# TODO: error checking using errno and == EOF


class FILE(object):
    def __init__(self, what, mode='r'):
        self._need_close = False
        if isinstance(what, (int, long)):
            self._as_parameter = _libc.fdopen(what, mode)
            self._need_close = True
            return
        if isinstance(what, basestring):
            self._as_parameter = _libc.fopen(what, mode)
            self._need_close = True
            return
        if isinstance(what, c_void_p):
            self._as_parameter = what
            self._need_close = False
            return
        raise NotImplementedError('do not know how to create FILE object', what)

    def close(self):
        _libc.fclose(self)
        del self._as_parameter
        self._need_close = False

    def __del__(self):
        if self._need_close:
            self.close()
