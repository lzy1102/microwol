import json

from pyChatGPT import ChatGPT
from ai.status import WorkingStatus, WorkingType
from ai.aibase import AiBase


class ChatAI(AiBase):
    def __init__(self, user, pwd, proxy):
        print("browsers", user)
        super().__init__()
        self.type = WorkingType.Browsers
        self.password = pwd
        self.user = user
        self.proxy = proxy
        self.api = ChatGPT(auth_type="openai", email=self.user, password=self.password, proxy=self.proxy,
                           chrome_args=['--no-sandbox', '--headless', '--disable-dev-shm-usage', '--disable-gpu',
                                        '--disable-gpu'])
        self.api.reset_conversation()
        self.user = user
        self.password = pwd
        self.api.reset_conversation()  # reset the conversation
        self.api.clear_conversations()  # clear all conversations
        self.api.refresh_chat_page()  # refresh the chat page
        # print(self.api.__session_token)
        # auth with openai login (manual captcha solving)
        # api = ChatGPT(
        #     auth_type='openai', captcha_solver=None,
        #     email='lzy575566430@gmail.com', password='lizhiyong575566'
        # )
        # auth with openai login (2captcha for captcha solving)
        # api = ChatGPT(
        #     auth_type='openai', captcha_solver='2captcha', solver_apikey='abc',
        #     email='example@gmail.com', password='password'
        # )
        # reuse cookies generated by successful login before login,
        # if `login_cookies_path` does not exist, it will process logining  with `auth_type`, and save cookies to `login_cookies_path`
        # only works when `auth_type` is `openai` or `google`
        # api = ChatGPT(auth_type='openai', email='example@xxx.com', password='password',
        #               login_cookies_path='your_cookies_path',
        #               )

        # resp = api.send_message('一份工作做了9年，该不该离开了？')
        # print(resp['message'])
        #
        # api.reset_conversation()  # reset the conversation
        # api.clear_conversations()  # clear all conversations
        # api.refresh_chat_page()  # refresh the chat page

    # def PwdApi(self, user: str, pwd: str, proxy: str):
    #     try:
    #         self.api = ChatGPT(auth_type="openai", email=self.user, password=self.password, proxy=self.proxy)
    #         self.api.reset_conversation()
    #         self.user = user
    #         self.password = pwd
    #         self.api.reset_conversation()  # reset the conversation
    #         self.api.clear_conversations()  # clear all conversations
    #         self.api.refresh_chat_page()  # refresh the chat page
    #         # print(self.api.__session_token)
    #         # auth with openai login (manual captcha solving)
    #         # api = ChatGPT(
    #         #     auth_type='openai', captcha_solver=None,
    #         #     email='lzy575566430@gmail.com', password='lizhiyong575566'
    #         # )
    #         # auth with openai login (2captcha for captcha solving)
    #         # api = ChatGPT(
    #         #     auth_type='openai', captcha_solver='2captcha', solver_apikey='abc',
    #         #     email='example@gmail.com', password='password'
    #         # )
    #         # reuse cookies generated by successful login before login,
    #         # if `login_cookies_path` does not exist, it will process logining  with `auth_type`, and save cookies to `login_cookies_path`
    #         # only works when `auth_type` is `openai` or `google`
    #         # api = ChatGPT(auth_type='openai', email='example@xxx.com', password='password',
    #         #               login_cookies_path='your_cookies_path',
    #         #               )
    #
    #         # resp = api.send_message('一份工作做了9年，该不该离开了？')
    #         # print(resp['message'])
    #         #
    #         # api.reset_conversation()  # reset the conversation
    #         # api.clear_conversations()  # clear all conversations
    #         # api.refresh_chat_page()  # refresh the chat page
    #     except Exception as e:
    #         print(e)

    def send(self, msg):
        super().send(msg=msg)
        print("浏览器工作了")
        self.status = WorkingStatus.Busy
        try:
            resp = self.api.send_message(msg)

            if len(resp['message']) > 400:
                for i in range(2):
                    t = self.api.send_message("继续")
                    last = resp['message']
                    resp['message'] = last + t['message']

            # print(resp['message'])
            # with open("resp.json", mode="w+", encoding="utf-8") as f:
            #     f.write(json.dumps(resp))
            # self.api.reset_conversation()  # reset the conversation
            # self.api.clear_conversations()  # clear all conversations
            # self.api.refresh_chat_page()  # refresh the chat page
            # {
            #   "message": "",
            #   "conversation_id": "3d66e60e-c989-4a6e-83f1-70d8c79bf295"
            # }

            return {'id': resp['conversation_id'], "message": resp['message']}
        except:
            self.api.refresh_chat_page()
            resp = self.api.send_message(msg)
            return {'id': resp['conversation_id'], "message": resp['message']}
        finally:
            self.status = WorkingStatus.Idle

# def init(user: str, pwd: str, proxy: str) -> ChatAI:
#     print("AI INIT")
#     chatai = ChatAI(user=user,pwd=pwd,proxy=proxy)
#     return chatai

# def main():
#     chatai = ChatAI()
#     chatai.PwdApi(user=args.user, pwd=args.pwd, proxy=args.proxy)
#     resp_msg = chatai.send("写一首关于春天下雪的五言绝句")
#     with open("result.txt", mode="w+", encoding="utf-8") as f:
#         f.write(resp_msg)
#     chatai.api.driver.close()
#     chatai.api.driver.quit()


# if __name__ == '__main__':
#     main()