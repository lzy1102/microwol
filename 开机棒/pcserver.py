import json
import random
import re
import time
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import hashlib
import paho.mqtt.client as mqtt

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///startup.db"
# initialize the app with the extension
db.init_app(app)


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)
# client.loop_forever()
client.loop_start()


# class StartUp(db.Model):
#     __tablename__ = "start_up"  # 指定表名称
#     id = db.Column(db.Integer, primary_key=True)
#     mac = db.Column(db.String, unique=True, nullable=False)
#     key = db.Column(db.String)
#     status = db.Column(db.String)


class Keys(db.Model):
    __tablename__ = "keys"  # 指定表名称
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, unique=True, nullable=False)


with app.app_context():
    db.create_all()


def validate_mac(value):
    if value.find('-') != -1:
        pattern = re.compile(r"^\s*([0-9a-fA-F]{2,2}-){5,5}[0-9a-fA-F]{2,2}\s*$")
        if pattern.match(value):
            return True
        else:
            return False
    if value.find(':') != -1:
        pattern = re.compile(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$")
        if pattern.match(value):
            return True
        else:
            return False


def isIP(ip_str):
    regular = re.compile('^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$')
    if regular.match(ip_str):
        return True
    else:
        return False


@app.route('/setstatus', methods=["GET"])
def set_status_mqtt():
    key = request.args.get("key")
    mac = request.args.get("mac")
    broadcast = request.args.get('broadcast')
    port = request.args.get('port')
    if mac == "" or mac is None or validate_mac(mac) is False:
        return "mac is null"
    if key == "" or key is None:
        return "key is null"
    if broadcast == "" or broadcast is None:
        return "broadcast is null"
    if isIP(broadcast) == False:
        return "broadcast not ip"

    tmp = Keys.query.filter_by(key=key).first()
    if tmp is None:
        return "not key"
    else:
        client.publish(topic=key, payload=json.dumps({"mac": mac, 'broadcast': broadcast, 'port': port}))
        return "ok"


@app.route('/getkey', methods=["GET"])
def getkey():
    key = request.args.get("key")
    tmp = Keys.query.filter_by(key=key).first()
    if tmp is None:
        shark = str(time.time_ns())+str(random.random())
        result = hashlib.md5(shark.encode()).hexdigest()
        db.session.add(Keys(key=result))
        db.session.commit()
        return result
    else:
        return tmp.key


# @app.route('/setstatus', methods=["GET"])
# def set_status():
#     status = request.args.get("status")
#     key = request.args.get("key")
#     mac = request.args.get("mac")
#     if mac == "" or mac is None or validate_mac(mac) is False:
#         return "mac is null"
#     if status != "0" and status != "1":
#         return "status is 0 or 1"
#     if key == "" or key is None:
#         return "key is null"
#     tmp = StartUp.query.filter_by(mac=mac, key=key).first()
#     if tmp is None:
#         return "not mac"
#     else:
#         tmp.status = status
#         db.session.commit()
#         return tmp.status


# @app.route('/getstatus')
# def get_status():
#     key = request.args.get("key")
#     mac = request.args.get("mac")
#     if mac == "" or mac is None or validate_mac(mac) is False:
#         return "mac is null"
#     if key == "" or key is None:
#         return "key is null"
#     tmp = StartUp.query.filter_by(mac=mac, key=key).first()
#     if tmp is None:
#         return "not mac"
#     else:
#         return tmp.status


# @app.route("/getkey", methods=["GET"])
# def get_key():
#     mac = request.args.get("mac")
#     if mac == "" or mac is None or validate_mac(mac) is False:
#         return "mac is null"
#
#     tmp = StartUp.query.filter_by(mac=mac).first()
#     if tmp is None:
#         shark = str(random.random())
#         result = hashlib.md5(str(mac + shark).encode()).hexdigest()
#         db.session.add(StartUp(mac=mac, key=result, status="0"))
#         db.session.commit()
#         return str(result)
#     else:
#         return tmp.key


if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=False)
