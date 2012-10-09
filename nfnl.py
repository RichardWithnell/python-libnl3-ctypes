#!/usr/bin/python
#coding: utf-8

from lib.ctypes.libnl3_nf import NETLINK_NETFILTER
from lib.nl3.netfilter.ctcache import NfNlCtCache
from lib.nl3.cachemgr import CacheMgr

def main():
    mngr = CacheMgr(protocol=NETLINK_NETFILTER)
    cache = mngr.add(NfNlCtCache)
    for ct in cache:
        print 'Begin', '-' * 80
        for direction in (0, 1):
            if ct.test_packets(direction):
                print ct.get_packets(direction)
            if ct.test_bytes(direction):
                print ct.get_bytes(direction)

if __name__ == '__main__':
    main()
