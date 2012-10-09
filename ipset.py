#!/usr/bin/python
#coding: utf-8
from lib.ctypes import ipset

from lib.nl3.netfilter.socket import Socket
from lib.nl3.netfilter.message import Message


def main():
    AF_INET = 2

    flags = ipset.IPSET_FLAGS[ipset.IPSET_CMD_LIST]
    msg = Message(ipset.NFNL_SUBSYS_IPSET, ipset.IPSET_CMD_LIST, flags, AF_INET, 0)
    msg.put_u8(ipset.IPSET_ATTR_PROTOCOL, ipset.IPSET_PROTOCOL)

    s = Socket()
    s.connect()
    s.send_auto_complete(msg)
    s.recvmsgs_default()

#resp:   attr:   IPSET_ATTR_SETNAME
#                IPSET_ATTR_TYPENAME
#                IPSET_ATTR_REVISION
#                IPSET_ATTR_FAMILY
#                IPSET_ATTR_DATA
#                        create-specific-data
#                IPSET_ATTR_ADT
#                        IPSET_ATTR_DATA
#                                adt-specific-data
#                        ...




if __name__ == '__main__':
    main()
