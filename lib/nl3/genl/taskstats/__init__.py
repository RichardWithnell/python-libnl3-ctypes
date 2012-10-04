#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from ctypes import Structure, c_uint16, c_uint32, c_uint8, c_uint64, c_char

from .socket import Socket
from ..ctrl.controller import CtrlCache


TASKSTATS_CMD_GET = 1
#TASKSTATS_VERSION = 8 # o_O some structs changes...
TASKSTATS_GENL_NAME = 'TASKSTATS'
TASKSTATS_GENL_VERSION = 1
TASKSTATS_CMD_ATTR_PID = 1
TASKSTATS_CMD_ATTR_REGISTER_CPUMASK = 3

TASKSTATS_TYPE_PID = 1
TASKSTATS_TYPE_TGID = 2
TASKSTATS_TYPE_STATS = 3
TASKSTATS_TYPE_AGGR_PID = 4
TASKSTATS_TYPE_AGGR_TGID = 5

TS_COMM_LEN = 32

#include <linux/taskstats.h> wrapper

#noinspection PyClassicStyleClass
class Taskstats_version_1(Structure):
    TASKSTATS_VERSION = 1

    #noinspection PyTypeChecker
    _fields_ = [
        ('version', c_uint16),
        ('ac_exitcode', c_uint32),
        ('ac_flag', c_uint8),
        ('ac_nice', c_uint8),
        ('_trash', c_uint8 * 6), # implementtion of next:
        ('cpu_count', c_uint64), # __attribute__((aligned(8)))
        ('cpu_delay_total', c_uint64),
        ('blkio_count', c_uint64),
        ('blkio_delay_total', c_uint64),
        ('swapin_count', c_uint64),
        ('swapin_delay_total', c_uint64),
        ('cpu_run_real_total', c_uint64),
        ('cpu_run_virtual_total', c_uint64),
        # version 1 ends here
        ('ac_comm', c_char * TS_COMM_LEN),
    ]

    def dump(self):
        for (name, _type) in self._fields_:
            if not name.startswith('_'):
                print '{0}={1}'.format(name, getattr(self, name))


def _resolve_family():
    with Socket() as sock:
        family = CtrlCache(sock).search_by_name(TASKSTATS_GENL_NAME)
    return (family.id_, family.hdrsize)


(family_id, family_hdrsize) = _resolve_family()

#################### version 1 ended here
#        char    ac_comm[TS_COMM_LEN]
#        __u8    ac_sched __attribute__((aligned(8)))
#        __u8    ac_pad[3]
#        __u32   ac_uid __attribute__((aligned(8)))
#        __u32   ac_gid
#        __u32   ac_pid
#        __u32   ac_ppid
#        __u32   ac_btime
#        __u64   ac_etime __attribute__((aligned(8)))
#        __u64   ac_utime
#        __u64   ac_stime
#        __u64   ac_minflt
#        __u64   ac_majflt
#        __u64   coremem
#        __u64   virtmem
#        __u64   hiwater_rss
#        __u64   hiwater_vm
#        __u64   read_char
#        __u64   write_char
#        __u64   read_syscalls
#        __u64   write_syscalls
#        __u64   read_bytes
#        __u64   write_bytes
#        __u64   cancelled_write_bytes
#        __u64  nvcsw
#        __u64  nivcsw
#        __u64   ac_utimescaled
#        __u64   ac_stimescaled
#        __u64   cpu_scaled_run_real_total
#        __u64   freepages_count
#        __u64   freepages_delay_total
#    ]

