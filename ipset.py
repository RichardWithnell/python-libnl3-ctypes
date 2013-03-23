#!/usr/bin/python
#coding: utf-8

from python_nl3.nl3.netfilter import ipset
from python_nl3.nl3.netfilter.socket import Socket
from python_nl3.nl3.netfilter.message import Message, nfnlmsg_alloc_simple

AF_INET = 2

def main():
    s = Socket()
    s.nfnl_connect()
    s.nl_send_auto_complete(ipset.nfnl_ipset_build_list_request(AF_INET, 'qwe'))
    s.nl_recvmsgs_default()

if __name__ == '__main__':
    main()
