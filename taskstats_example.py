#!/usr/bin/python
#coding: utf-8

#from __future__ import absolute_import
from _ctypes import sizeof

import select
from lib.ctypes.taskstats import *
from lib.nl3.genl.taskstats.struct import Taskstats_version_1
from lib.nl3.genl.taskstats.socket import Socket
from lib.nl3.socket import NL_CB_VALID, NL_CB_CUSTOM

class Application(object):
    def _callback(self, message):
        nlhdr = message.hdr()
        if not nlhdr.valid_hdr():
            raise Exception('Internal error')
        for attr in nlhdr.hdr():
            attr_type = attr.type()

            if  attr_type not in (TASKSTATS_TYPE_AGGR_PID, TASKSTATS_TYPE_AGGR_TGID):
                raise Exception('Nested (outer) attr is of invalid type', attr_type)

            for attr in attr.attributes():
                attr_type = attr.type()

                if attr_type == TASKSTATS_TYPE_PID:
                    print 'Dead pid is:', attr.u32
                    continue

                if attr_type == TASKSTATS_TYPE_TGID:
                    print 'Dead tgid is:', attr.u32
                    continue

                if attr_type == TASKSTATS_TYPE_STATS:
                    length = attr.len()
                    size = sizeof(Taskstats_version_1)
                    if length < size:
                        raise ValueError('Not enought data to build structure. Required at least %d, passed %d', size,
                            length)
                    data = attr.data()
                    #noinspection PyUnresolvedReferences
                    info = Taskstats_version_1.from_address(data)
                    info.dump()
                    continue

                raise Exception('Unknown type in inner attributes', attr_type)
            print '-' * 80

    def do_poll(self):
        with Socket() as sock:
            sock.register_cpumask()
            sock.modify_cb(NL_CB_VALID, NL_CB_CUSTOM, self._callback)

            # in order to able to interrupt process, we will poll() socket instead of blocking recv()
            # when python inside ctypes's function, SIGINT handling is suspended
            sock.set_nonblocking()
            poller = select.poll()
            poller.register(sock, select.POLLIN)
            while poller.poll():
                sock.recvmsgs_default()


def main():
    Application().do_poll()

if __name__ == '__main__':
    main()
