#!/usr/bin/python
#coding: utf-8

from python_nl3.nl3.netfilter import ipset
from python_nl3.nl3.netfilter.socket import Socket
from python_nl3.nl3.netfilter.message import Message, nfnlmsg_alloc_simple


def main():
    AF_INET = 2

    msgptr = nfnlmsg_alloc_simple(ipset.NFNL_SUBSYS_IPSET, ipset.IPSET_CMD_LIST, ipset.IPSET_FLAGS[ipset.IPSET_CMD_LIST], AF_INET, 0)
    msg = Message(msgptr)
    msg.nla_put_u8(ipset.IPSET_ATTR_PROTOCOL, ipset.IPSET_PROTOCOL)

    s = Socket()
    s.nfnl_connect()
    s.nl_send_auto_complete(msg)
    s.nl_recvmsgs_default()

if __name__ == '__main__':
    main()
