#!/usr/bin/env python
# Created by iFantastic on 2023/2/10
import re
from enum import Enum


class WorkingStatus(Enum):
    Idle = 0  #
    Busy = 1


class WorkingType(Enum):
    Browsers = 0
    Api = 1


class Reply(Enum):
    Normal = 0
    Error = 1


def CheckMessage(msg):
    reList = ["无法回答", "作为一个人工智能", "我是一个人工智能程序", "未知。", "抱歉，", "无法回答", "对不起", "我是AI", "很抱歉",
              "我不知道"]
    for item in reList:
        match = re.search(item, msg)
        if match:
            return Reply.Error
    return Reply.Normal


if __name__ == '__main__':
    pass
