#!/usr/bin/env python
# Created by iFantastic on 2023/2/9
import json

import openai
from ai.aibase import AiBase
from ai.status import WorkingStatus, WorkingType


class ApiAI(AiBase):

    def __init__(self, organization, key):
        super().__init__()
        print("token", key)
        self.type = WorkingType.Api
        self.key = key
        openai.organization = organization
        openai.api_key = key
        # list engines
        # engines = openai.Engine.list()
        # Note: you need to be using OpenAI Python v0.27.0 for the code below to work

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
            completion = openai.ChatCompletion.create(
                api_key=self.key,
                model="gpt-3.5-turbo",
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant."},
                    # {"role": "user", "content": "Who won the world series in 2020?"},
                    # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                    {"role": "user", "content": msg}
                ]
            )
            return {'id': completion['id'], "message": completion.choices[0].message.content}
            # completion = openai.Completion.create(engine="text-davinci-003", prompt=msg, max_tokens=4000,
            #                                       temperature=0.5)
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
    aai = ApiAI(organization="", key="")
    print(aai.key)
    print(aai.status)
    print(aai.send(msg="如何提高工作效率用中文回答"))
