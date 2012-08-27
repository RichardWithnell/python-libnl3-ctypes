#!/usr/bin/python
#coding: utf-8

from python_nl3.nl3.netfilter.socket  import Socket
from python_nl3.nl3.netfilter.ctcache  import NfNlCtCache

def main():
    sock = Socket()
    sock.nfnl_connect()

    cache = NfNlCtCache(sock)

    for ct in cache:
        print 'Begin', '-' * 80
        for direction in (0, 1):
            if ct.nfnl_ct_test_packets(direction):
                print ct.nfnl_ct_get_packets(direction)
            if ct.nfnl_ct_test_bytes(direction):
                print ct.nfnl_ct_get_bytes(direction)

if __name__ == '__main__':
    main()
