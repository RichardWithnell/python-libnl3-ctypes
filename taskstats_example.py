#!/usr/bin/python
#coding: utf-8

#from __future__ import absolute_import
from _ctypes import sizeof

import select

from lib.nl3.socket                    import NL_CB_VALID, NL_CB_CUSTOM
from lib.nl3.genl                      import taskstats

# Produce taskstats messages
from lib.nl3.genl.taskstats.socket     import Socket

class Application(object):
    def _callback(self, message):
        nlhdr = message.nlmsg_hdr()
        if not nlhdr.genlmsg_valid_hdr():
            raise Exception('Internal error')
        ghdr = nlhdr.genlmsg_hdr()
        for attr in ghdr:
            attr_type = attr.nla_type()

            if  attr_type not in (taskstats.TASKSTATS_TYPE_AGGR_PID, taskstats.TASKSTATS_TYPE_AGGR_TGID):
                raise Exception('Nested (outer) attr is of invalid type', attr_type)

            for attr in attr.attributes():
                attr_type = attr.nla_type()

                if attr_type == taskstats.TASKSTATS_TYPE_PID:
                    print 'Dead pid is:', attr.nla_get_u32()
                    continue

                if attr_type == taskstats.TASKSTATS_TYPE_TGID:
                    print 'Dead tgid is:', attr.nla_get_u32()
                    continue

                if attr_type == taskstats.TASKSTATS_TYPE_STATS:
                    length = attr.len()
                    size = sizeof(taskstats.Taskstats_version_1)
                    if length < size:
                        raise ValueError('Not enought data to build structure. Required at least %d, passed %d', size,
                            length)
                    data = attr.data()
                    #noinspection PyUnresolvedReferences
                    info = taskstats.Taskstats_version_1.from_address(data)
                    info.dump()
                    continue

                raise Exception('Unknown type in inner attributes', attr_type)
            print '-' * 80

    def do_poll(self):
        with Socket() as sock:
            sock.task_register_cpumask()
            sock.nl_socket_modify_cb(NL_CB_VALID, NL_CB_CUSTOM, self._callback)

            # in order to able to interrupt process, we will poll() socket instead of blocking recv()
            # when python inside ctypes's function, SIGINT handling is suspended
            sock.nl_socket_set_nonblocking()
            poller = select.poll()
            poller.register(sock, select.POLLIN)
            while poller.poll():
                sock.nl_recvmsgs_default()


def main():
    Application().do_poll()

if __name__ == '__main__':
    main()
