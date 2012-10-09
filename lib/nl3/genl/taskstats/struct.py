# coding=utf-8

from __future__ import absolute_import

from ....ctypes.taskstats import Taskstats_version_1 as Taskstats_version_1_

#noinspection PyClassicStyleClass
class Taskstats_version_1(Taskstats_version_1_):
    def dump(self):
        for (name, _type) in self._fields_:
            if not name.startswith('_'):
                print '{0}={1}'.format(name, getattr(self, name))
