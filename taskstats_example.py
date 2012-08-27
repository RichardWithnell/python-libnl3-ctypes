#!/usr/bin/python
#coding: utf-8

#from __future__ import absolute_import

from python_nl3.nl3.genl.socket     import Socket
from python_nl3.nl3.socket          import NL_CB_MSG_IN, NL_CB_CUSTOM
from python_nl3.nl3.genl.message    import Message
from python_nl3.nl3.genl.controller import CtrlCache
from python_nl3.nl3  import NL_AUTO_PORT, NL_AUTO_SEQ
from python_nl3      import taskstats
import select
import sys

class Application(object):
    def __init__(self):
        self.outfile = None

        sock = Socket()
        sock.genl_connect()
        family = CtrlCache(sock).genl_ctrl_search_by_name(taskstats.TASKSTATS_GENL_NAME)
        #family_id = genl_ctrl_resolve(sock, taskstats.TASKSTATS_GENL_NAME)
        self.family_id = family.id_
        self.family_hdrsize = family.hdrsize

    def prepare_death_message(self):
        # multiprocessing.cpu_count() may be used for that, but we really need only online CPUS, anot not 0-{count}
        with open('/sys/devices/system/cpu/online', 'rt') as cpus_file:
            cpumask = cpus_file.read()

        msg = Message()
        msg.genlmsg_put(NL_AUTO_PORT, NL_AUTO_SEQ, self.family_id, 0, 0, taskstats.TASKSTATS_CMD_GET, taskstats.TASKSTATS_GENL_VERSION)
        msg.nla_put_string(taskstats.TASKSTATS_CMD_ATTR_REGISTER_CPUMASK, cpumask)
        return msg

    def _callback(self, message):
        nlhdr = message.nlmsg_hdr()
        if not nlhdr.genlmsg_valid_hdr(self.family_hdrsize):
            raise Exception('Internal error')
        ghdr = nlhdr.genlmsg_hdr(self.family_hdrsize)
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
                    info = taskstats.from_data(attr.nla_data(), attr.nla_len())
                    info.dump()
                    continue

                raise Exception('Unknown type in inner attributes', attr_type)
            print '-' * 80

    def do_poll(self):
        sock = Socket()
        sock.genl_connect()

        sock.nl_send_auto_complete(self.prepare_death_message())
        sock.nl_wait_for_ack()

        # http://www.infradead.org/~tgr/libnl/doc/core.html#core_sk_seq_num
        sock.nl_socket_disable_seq_check()

        sock.nl_socket_modify_cb(NL_CB_MSG_IN, NL_CB_CUSTOM, self._callback)

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
