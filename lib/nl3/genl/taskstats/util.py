#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import


def get_all_cpus():
    # multiprocessing.cpu_count() may be used for that, but we really need only online CPUS, anot not 0-{count}
    with open('/sys/devices/system/cpu/online', 'rt') as cpus_file:
        return cpus_file.read()
