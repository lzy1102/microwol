import json
import os
import random
import time
from datetime import timedelta

import yaml
from flask import Flask
from flask import request
from flask_cors import CORS
import ai.pool
from dbutil import db as mongo, model
from ai.status import WorkingStatus
import queue, uuid
import threading
from cacheout import Cache

cache = Cache(maxsize=1000, ttl=1000)
msg_queue = queue.Queue()
ai_queue = queue.Queue()

aiPool = ai.pool.AiPool(cfgpath="config.yaml").poolMap
for k, v in aiPool.items():
    ai_queue.put(item=k)


# 定义一个生产者函数，用于向队列中添加数据
def producer():
    while True:
        if msg_queue.empty():
            time.sleep(2)
            continue
        data = msg_queue.get()
        threading.Thread(target=consumer, args=(data,)).start()


# 定义一个消费者函数，用于从队列中取出并处理数据
def consumer(msg_data):
    while True:
        if ai_queue.empty() is False:
            tmpai = ai_queue.get()
            break
        time.sleep(1)
    resp = aiPool[tmpai].send2(msg=msg_data["msg"])
    ai_queue.put(item=tmpai)
    cache.add(key=msg_data["id"], value=resp)


# 创建生产者和消费者线程，并启动它们
producer_thread = threading.Thread(target=producer)
producer_thread.start()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 配置1天有效

# 判断是否加入到数据库
if os.path.exists('db.yaml'):
    with open("db.yaml", mode="r+", encoding="utf-8") as f:
        db_cfg = yaml.load(f, yaml.FullLoader)
        # app.config["MONGO_URI"] = db_cfg["uri"]
        db = mongo.DB(uri=db_cfg['uri'], dbname=db_cfg['dbname'])
CORS(app, resources=r'/*')
app.config['timeout'] = 60 * 60


@app.route("/api/msg/put", methods=['POST'])
def msg_put():
    # msg = request.form.get("msg")
    # driver = request.form.get("driver")

    msg_data = request.get_data()
    if msg_data is None or msg_data == "":
        return {"msg": [], "id": "", "remark": ""}
    msg_data = json.loads(msg_data)
    try:
        remark = msg_data["remark"]
    except:
        remark = None
    msg = msg_data["msg"]
    uid = uuid.uuid4()
    data = {"msg": msg, "id": str(uid), "remark": remark}
    # print(model.BaiduMsg(msg=msg, remark=remark).__dict__)
    print(data)
    if db is not None and remark is not None and remark != "":
        msg_data["create_at"] = time.time()
        find_result = db.find_one("msg", {"remark": remark, "msg": {"$all": msg}})
        if find_result is not None:
            data["status"] = "over"
            return data, 200
        else:
            db.insert_one("msg", msg_data)
    msg_queue.put(item=data)
    data["status"] = "ok"
    return data, 200


@app.route("/api/msg/get", methods=['POST'])
def msg_get():
    # id = request.form.get("id")
    msg_data = request.get_data()
    if msg_data is None or msg_data == "":
        return {"msg": [], "id": "", "remark": ""}
    msg_data = json.loads(msg_data)
    id = msg_data["id"]
    remark = msg_data["remark"]
    if id in cache.keys():
        data = cache.get(id)
        cache.delete(id)
        have = False
        for i in data:
            msg_tmp = i
            if ai.status.CheckMessage(msg_tmp) == ai.status.Reply.Error:
                have = True
                break
        if have:
            return {"id": id, "msg": data, "remark": remark, "status": "error"}, 200
        else:
            return {"id": id, "msg": data, "remark": remark, "status": "ok"}, 200
    else:
        return {"id": id, "remark": remark, "status": "wait"}, 200


@app.route("/api/conversation", methods=['POST'])
def conversation():
    set_config = request.get_data()
    if set_config is None or set_config == "":
        return []
    set_config = json.loads(set_config)
    msg = set_config['message']
    print(msg)
    while True:
        if ai_queue.empty() is False:
            tmpai = ai_queue.get()
            break
        time.sleep(1)
        # print("没有空闲的", ai_queue.qsize())
    resp = aiPool[tmpai].send(msg=msg)
    ai_queue.put(item=tmpai)
    print(resp)
    conversationId = uuid.uuid4()
    cache.add(conversationId, msg)
    result = {"message": resp['message'], "conversationId": conversationId,
              "parentMessageId": set_config["conversationId"]}
    return result, 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
