#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ..nlmsghdr import NlMsgHdr as NlMsgHdr_
from . import family_hdrsize

class NlMsgHdr(NlMsgHdr_):
    _family_hdrsize = family_hdrsize
