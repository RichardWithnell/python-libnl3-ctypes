#!/usr/bin/env python
#coding: utf-8

from __future__ import absolute_import

from ctypes import cdll
from ctypes.util import find_library

genl = cdll.LoadLibrary(find_library('nl-genl-3'))
