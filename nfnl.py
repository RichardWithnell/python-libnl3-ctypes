#!/usr/bin/python
#coding: utf-8

from lib.ctypes.libnl3_nf import NETLINK_NETFILTER
from lib.nl3.netfilter.ctcache import NfNlCtCache
from lib.nl3.cachemgr import CacheMgr

def main():
    mngr = CacheMgr(None, NETLINK_NETFILTER)
    cache = mngr.add(NfNlCtCache)
    for ct in cache:
        print 'Begin', '-' * 80
        for direction in (0, 1):
            if ct.nfnl_ct_test_packets(direction):
                print ct.nfnl_ct_get_packets(direction)
            if ct.nfnl_ct_test_bytes(direction):
                print ct.nfnl_ct_get_bytes(direction)

if __name__ == '__main__':
    main()
