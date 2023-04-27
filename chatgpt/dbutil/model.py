#!/usr/bin/env python
# Created by iFantastic on 2023/4/23
import datetime


class BaiduMsg:
    def __init__(self, msg, remark):
        self.msg = msg
        self.remark = remark
        self.create_at = datetime.datetime.now()


if __name__ == '__main__':
    pass
