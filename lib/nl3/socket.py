#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

import traceback
from ..ctypes.libnl3 import *
from .message import Message


class Socket(object):
    _message_class = Message
    _protocol = None

    def __init__(self, protocol=None):
        self._need_free = False
        self.__cb_storage = dict()
        self._as_parameter_ = nl_socket_alloc()
        self._need_free = True
        self._protocol = protocol

    close = lambda self: nl_close(self)
    wait_for_ack = lambda self: nl_wait_for_ack(self)
    set_nonblocking = lambda self: nl_socket_set_nonblocking(self)
    disable_seq_check = lambda self: nl_socket_disable_seq_check(self)
    recvmsgs_default = lambda self: nl_recvmsgs_default(self)
    send_auto_complete = lambda self, msg: nl_send_auto_complete(self, msg)
    get_fd = lambda self: nl_socket_get_fd(self)

    def connect(self):
        proto = self._protocol
        if proto is None:
            raise RuntimeError(
                'You should specify protocol for this socket (in constructor) or choose another socket class')
        nl_connect(self, proto)

    def modify_cb(self, type_, kind, func):
        """ expect function without parameters. Use closure to make usage of additional data """

        msgcls = self._message_class

        #noinspection PyUnusedLocal
        def c_callback(msg, _void_ptr):
            #noinspection PyBroadException
            try:
                ret = func(msgcls(ptr=msg, parent=self))
                return NL_OK if ret is None else int(ret)
            except:
                traceback.print_exc()
                return NL_STOP

        callback = nl_recvmsg_msg_cb_t(c_callback)
        ret = nl_socket_modify_cb(self, type_, kind, callback, None)
        self.__cb_storage[(type_, kind)] = callback # prevent from callback garbage collection.
        return ret

    fileno = get_fd

    def _free(self):
        nl_socket_free(self)
        del self._as_parameter_

    def __del__(self):
        if self._need_free:
            self._free()
            self._need_free = False

    def __enter__(self):
        if self.get_fd() != -1:
            raise RuntimeError('Socket already connected')
        self.connect()
        return self

    #noinspection PyUnusedLocal
    def __exit__(self, _type, value, tb):
        self.close()
