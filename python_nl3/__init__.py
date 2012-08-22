#!/usr/bin/python
#coding: utf-8

import os

from ctypes import c_int, c_byte, c_void_p, cdll, c_char_p, CFUNCTYPE, c_uint32, c_uint8
from ctypes.util import find_library

def swrap(library, errcheck, restype, *argtypes):
    """
    Специальный декоратор.
    Результат оборачивания  - НЕ ФУНКЦИЯ!

    поэтому она не становиться instancemethod после чтого как класс объявлен
    """
    def decorator(original):
        result = getattr(library, original.func_name)
        if errcheck is not None:
            result.errcheck = errcheck
        result.restype = restype
        result.argtypes = argtypes
        return result
    return decorator


def nullptr_check(result, func, args):
    if result == 0:
        raise Exception('Allocation failure', result, func, args)
    return result

class StdNL(object):
    """
    Base class for all object, that allocates using nl_*_allocate()
    """
    def __init__(self, ptr=None):
        if ptr is None:
            self._as_parameter_ = self._alloc_ptr()
            self._free = self._free_ptr
        else:
            self._as_parameter_ = ptr

    def __del__(self):
        _free = getattr(self, '_free', None)
        if _free is not None:
            _free(self)

