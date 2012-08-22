#!/usr/bin/python
#coding: utf-8

import os

from .. import swrap
from ctypes import c_int, c_byte, c_void_p, cdll, c_char_p, CFUNCTYPE, c_uint32, c_uint8
from ctypes.util import find_library
nl = cdll.LoadLibrary(find_library('nl-3'))

#TODO: move to separate modules
NL_AUTO_PORT = 0
NL_AUTO_SEQ = 0
NLM_F_REQUEST = 1

def wrap(*args):
    """
    Специальный декоратор, результат оборачивания - функция,
    которая может стать instancemethod'ом

    Смысл - API libnl в качестве первого аргумента при реализации OOП посылает как казатель объекта
    Таким образом, это очень похоже на self

    Когда вызывают object.method(x, y, ...) производится object.__class__.method(object, x, y,...)

    таким образом, в результат оборачивания в первом аргументе идёт сам объект,
    а пользуясь свойством ctypes: _as_parameter_ оно превращается в указатель (заренее сохранённый)
    (см. класс StdNL)

    """
    sdecorator = swrap(*args)
    def decorator(original):
        result = sdecorator(original)
        # Так как isinstance(result, Function) is False
        # То он автоматически не превращается в Instancemethod
        # Поэтому, сделаем обёртку
        method = lambda *args2: result(*args2)
        method.func_name = original.func_name
        method.__dict__.update(original.__dict__)
        return method
    return decorator

def fwrap(*args):
    sdecorator = swrap(*args)
    def decorator(original):
        result = sdecorator(original)
        # Так как isinstance(result, Function) is False
        # То он автоматически не превращается в Instancemethod
        # Поэтому, сделаем обёртку
        method = lambda self, *args2: original(self, result(self, *args2))
        method.func_name = original.func_name
        method.__dict__.update(original.__dict__)
        return method
    return decorator

@swrap(nl, None, c_char_p, c_int)
def nl_geterror(): pass

def errcode_check(result, func, args):
    if result < 0:
        raise Exception(nl_geterror(result), result, func, args)
    return result
