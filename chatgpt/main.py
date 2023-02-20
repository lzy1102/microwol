import json
import os
import random
from datetime import timedelta

from flask import Flask
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo
from pywebio.input import *
from pywebio.output import *
from pywebio.platform.flask import webio_view

import ai.pool
from ai.status import WorkingStatus

aiPool = ai.pool.AiPool(cfgpath="config.yaml").poolMap

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 配置1天有效
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)
CORS(app, resources=r'/*')
app.config['timeout'] = 60 * 60
aiList = [i for i in aiPool.values()]


@app.route("/api/conversation", methods=['POST'])
def send():
    set_config = request.get_data()
    if set_config is None or set_config == "":
        return []
    set_config = json.loads(set_config)

    # msg = request.form.get("msg")
    msg = set_config['message']
    print(msg)

    while True:
        aiIndex = random.randint(0, len(aiList) - 1)
        aiObj = aiList[aiIndex]
        if aiObj.status == WorkingStatus.Idle:
            tmpai = aiObj
            break

    # for i in aiPool.values():
    #     if i.status == WorkingStatus.Idle:
    #         tmpai = i
    #         break
    resp = tmpai.send(msg=msg)
    print(resp)
    result = {"message": resp['message'], "conversationId": resp['id'], "parentMessageId": set_config["conversationId"]}
    return result, 200


def chat():
    put_markdown('## PyWebIO Chat')
    while True:
        user_input = input("Your message:", type=TEXT)
        put_markdown("img/you.jpg: " + user_input)
        # tmpai = None
        while True:
            aiIndex = random.randint(0, len(aiList) - 1)
            aiObj = aiList[aiIndex]
            if aiObj.status == WorkingStatus.Idle:
                tmpai = aiObj
                break
        resp = tmpai.send(msg=user_input)
        received_msg = resp['message']
        put_markdown("img/ai.png: " + received_msg)
        put_text("**************************************************************************************************")


if __name__ == '__main__':
    app.add_url_rule('/', 'webio_view', webio_view(chat), methods=['GET', 'POST'])
    app.run(host="0.0.0.0", port=5000)
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # server.serve_forever()
