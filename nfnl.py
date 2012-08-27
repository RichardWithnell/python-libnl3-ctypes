#!/usr/bin/python
#coding: utf-8

import python_nl3.nl3.netfilter.ctcache
from python_nl3.nl3.netfilter import NETLINK_NETFILTER
from python_nl3.nl3.cachemgr import CacheMgr

def main():
    mngr = CacheMgr(None, NETLINK_NETFILTER)
    cache = mngr.nl_cache_mngr_add('netfilter/ct')
    for ct in cache:
        print 'Begin', '-' * 80
        for direction in (0, 1):
            if ct.nfnl_ct_test_packets(direction):
                print ct.nfnl_ct_get_packets(direction)
            if ct.nfnl_ct_test_bytes(direction):
                print ct.nfnl_ct_get_bytes(direction)

if __name__ == '__main__':
    main()
