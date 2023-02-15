#!/usr/bin/env python
# Created by iFantastic on 2023/2/10
import time

import yaml
from ai.chatai import ChatAI
from ai.apiapi import ApiAI
from ai.status import WorkingStatus, WorkingType


class AiPool(object):
    def __init__(self, cfgpath):
        with open(cfgpath, mode="r+", encoding="utf-8") as f:
            config = yaml.load(f, yaml.FullLoader)
        self.poolMap = {}
        print(config, "browsers" in config and len(config['browsers']) > 0)
        if "browsers" in config and len(config['browsers']) > 0:
            for browser in config['browsers']:
                self.poolMap[browser['user']+"_browser"] = ChatAI(user=browser['user'], pwd=browser['password'],
                                                       proxy=browser['proxy'])
        else:
            # api
            for api in config['keys']:
                self.poolMap[api['user']+"_key"] = ApiAI(key=api['key'])


if __name__ == '__main__':
    po = AiPool(cfgpath="../config.yaml")

    for i in po.poolMap.values():
        if i.status == WorkingStatus.Idle:
            print(i.send(msg="写一个春天下雪的诗"))
