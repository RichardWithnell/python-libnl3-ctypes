# coding=utf-8

from __future__ import absolute_import

from ctypes import CDLL, c_void_p, c_char_p, c_int

# monkey-patch __repr__ in that way:

#def _ctypes_func_repr(self):
#    #return '<ctypes: {0}: {1}()>'.format(self._libname, self._funcname)
#    # Warning: in common case __name__ may be undefined (if function loaded by ordinal)
#    return '<{}()>'.format(self.__name__)
#
#class MYDLL(CDLL):
#    def __init__(self, *args, **kwargs):
#        #noinspection PyArgumentList
#        super(MYDLL, self).__init__(*args, **kwargs)
#        self._FuncPtr.__repr__ = _ctypes_func_repr

MYDLL = CDLL

# USE _findSoname_ldconfig instead of find_library to guess library name
# from ctypes.util import _findSoname_ldconfig
#def find_library(name):
#    result = _findSoname_ldconfig(name)
#    if result is None:
#        raise RuntimeError('Library {!r} not found'.format(name))
#    log.info('Found ctypes library %r by name %r', result, name)
#    return result

def profile_that(result, func_name, lib_name):
    result2 = lambda *args: result(*args)
    codeobj = result2.func_code
    codeobj = codeobj.__class__(
        codeobj.co_argcount,
        codeobj.co_nlocals,
        codeobj.co_stacksize,
        codeobj.co_flags,
        codeobj.co_code,
        codeobj.co_consts,
        codeobj.co_names,
        codeobj.co_varnames,
        #[],#freevars,
        #[],#cellvars,
        codeobj.co_filename,
        'ctypes {0}: {1}'.format(lib_name, func_name), #codeobj.co_name,
        codeobj.co_firstlineno,
        codeobj.co_lnotab,
        ('result',),
        tuple()
    )
    result2.func_code = codeobj
    return result2


def common_loader(original, errcheck, restype, library, *argtypes):
    #print 'Defining {0} {1}({2})'.format(restype.__name__ if restype is not None else 'void', original.func_name, ', '.join((i.__name__ for i in argtypes)))
    func_name = original.func_name
    result = getattr(library, func_name)
    if errcheck is not None:
        result.errcheck = errcheck
    result.restype = restype
    result.argtypes = argtypes
    result.__doc__ = original.__doc__
    #return profile_that(result, func_name, library._name)
    return result


class NullPointerException(Exception):
    pass


def nullptr_check(result, func, args):
    if result == 0:
        raise NullPointerException('NULL pointer in result', result, func, args)
    return result


def wrap_ptr(*args):
    return lambda original: common_loader(original, nullptr_check, c_void_p, *args)


def wrap_ptr_no_check(*args):
    return lambda original: common_loader(original, None, c_void_p, *args)


def wrap_char_ptr(*args):
    return lambda original: common_loader(original, nullptr_check, c_char_p, *args)


def wrap_char_ptr_no_check(*args):
    return lambda original: common_loader(original, None, c_char_p, *args)


def wrap_void(*args):
    return lambda original: common_loader(original, None, None, *args)


def wrap_int(*args):
    return lambda original: common_loader(original, None, c_int, *args)

# wrap custom types without check
def wrap_custom(lib, custom, *args):
    return lambda original: common_loader(original, None, custom, lib, *args)

