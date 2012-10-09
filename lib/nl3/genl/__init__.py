# coding=utf-8

# TODO: actually, done at first message construction
from .ctrl.controller import CtrlCache

def resolve_family(name):
    family = CtrlCache().search_by_name(name)
    return (family.id, family.hdrsize)
