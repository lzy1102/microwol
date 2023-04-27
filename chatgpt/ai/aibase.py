#!/usr/bin/env python
# Created by iFantastic on 2023/2/10

from ai.status import WorkingStatus, WorkingType


class AiBase(object):
    def __init__(self):
        self.status = WorkingStatus.Idle
        self.type = WorkingType.Api

    def send(self, msg):
        pass

    def send2(self, msg):
        pass


if __name__ == '__main__':
    pass
