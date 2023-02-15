import json
import os
from datetime import timedelta

from flask import Flask
from flask import request
from flask_cors import CORS
from pywebio.input import *
from pywebio.output import *
from pywebio.platform.flask import webio_view

import ai.pool
from ai.status import WorkingStatus

aiPool = ai.pool.AiPool(cfgpath="config.yaml").poolMap

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 配置1天有效
CORS(app, resources=r'/*')


# @app.route("/", methods=['GET'])
# def index():
#     return "hello ai"


@app.route("/conversation", methods=['POST'])
def send():
    print(request.method)
    set_config = request.get_data()
    print(set_config)
    if set_config is None or set_config == "":
        return []
    set_config = json.loads(set_config)
    print(set_config)

    # msg = request.form.get("msg")
    msg = set_config['message']
    tmpai = "None"
    # return set_config
    for i in aiPool.values():
        if i.status == WorkingStatus.Idle:
            tmpai = i
            break
    resp = tmpai.send(msg=msg)
    print(resp)
    result = {"message": resp['message'], "conversationId": resp['id'], "parentMessageId": set_config["conversationId"]}
    return result, 200


def chat():
    put_markdown('## PyWebIO Chat')
    while True:
        user_input = input("Your message:", type=TEXT)
        put_text("You: " + user_input)

        tmpai = None
        for i in aiPool.values():
            if i.status == WorkingStatus.Idle:
                tmpai = i
                break
        resp = tmpai.send(msg=user_input)
        received_msg = resp['message']
        put_text("AI: " + received_msg)


if __name__ == '__main__':
    app.add_url_rule('/', 'webio_view', webio_view(chat), methods=['GET', 'POST'])
    app.run(host="0.0.0.0", port=5000)
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # server.serve_forever()
