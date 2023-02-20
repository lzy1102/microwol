#!/usr/bin/env python
# Created by iFantastic on 2023/2/9
import json

import openai
from ai.aibase import AiBase
from ai.status import WorkingStatus, WorkingType


class ApiAI(AiBase):

    def __init__(self, key):
        super().__init__()
        print("token",key)
        self.type = WorkingType.Api
        self.key = key
        openai.api_key = key
        # list engines
        engines = openai.Engine.list()
        # print the first engine's id
        # print(engines)

    def send(self, msg):
        super().send(msg=msg)
        self.status = WorkingStatus.Busy
        print("API 工作了")
        # create a completion
        # temperature  准确性  ，0 最高 ，1最低
        # max_tokens  结果长度
        try:
            # text-davinci-003
            # text-davinci-002-render
            completion = openai.Completion.create(engine="text-davinci-003", prompt=msg, max_tokens=4000,
                                                  temperature=0.5)
            # print the completion
            # with open("completion.json", mode="w+", encoding="utf-8") as f:
            #     f.write(json.dumps(completion))
            # print(completion.choices[0].text)
            return {'id': completion['id'], "message": completion.choices[0].text}
        except Exception as e:
            print(e)
            return {'id': "", "message": ""}
        finally:
            self.status = WorkingStatus.Idle


if __name__ == '__main__':
    aai = ApiAI(key="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")
    print(aai.key)
    print(aai.status)
    print(aai.send(msg="如何提高工作效率用中文回答"))
