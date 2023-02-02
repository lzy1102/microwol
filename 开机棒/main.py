import socket

import json

import machine
import network
import time
from machine import Pin
import ustruct

led1 = Pin(12, Pin.OUT)
led1.off()
led2 = Pin(13, Pin.OUT)
led2.off()

SERVER = 'broker.emqx.io'  # broker.mqttdashboard.com
TOPIC = 'e9300a23c399722f4107ea1e457a6367'.encode()
ssid = "yangdabao"
password = "lizhiyong418"


def connectWifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    wlan.disconnect()
    wlan.connect(ssid, password)  # connect to an AP
    time.sleep(5)  # 等待几秒，要不然isconnected 一直是false
    if wlan.isconnected():
        print(wlan.ifconfig())  # get the interface's IP/netmask/gw/DNS addresses


def wake_up(mac='E0-D5-5E-7D-B9-EA', broadcast="192.168.1.255", port=9):
    if len(mac) != 17:
        raise ValueError("MAC address should be set as form 'XX-XX-XX-XX-XX-XX'")
    mac_address = mac.replace("-", '')
    data = ''.join(['FFFFFFFFFFFF', mac_address * 20])  # 构造原始数据格式
    send_data = b''

    # 把原始数据转换为16进制字节数组，
    for i in range(0, len(data), 2):
        send_data = b''.join([send_data, ustruct.pack('B', int(data[i: i + 2], 16))])
    print(send_data)

    # 通过socket广播出去，为避免失败，间隔广播三次
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.sendto(send_data, (broadcast, port))
        time.sleep(1)
        sock.sendto(send_data, (broadcast, port))
        time.sleep(1)
        sock.sendto(send_data, (broadcast, port))
        sock.close()
        print("Done")
    except Exception as e:
        print(e)


def mqtt_callback(topic, msg):
    try:
        data = json.loads(msg.decode())
        print("开机")
        print(data)
        led2.on()
        led1.on()
        if topic == TOPIC:
            wake_up(mac=data['mac'], broadcast=data['broadcast'], port=int(data['port']))
            time.sleep(1)
        led1.off()
        led2.off()
    except Exception as e:
        print("err", e)
        led1.off()
        led2.off()


def main():
    try:
        global urequests, MQTTClient
        connectWifi(ssid=ssid, password=password)
        try:
            import urequests
            from umqtt.simple import MQTTClient
        except:
            import upip
            upip.install("urequests")
            upip.install('micropython-umqtt.simple')
        client = MQTTClient(client_id=TOPIC, server=SERVER, port=1883, keepalive=60)
        client.set_callback(mqtt_callback)
        client.connect()
        client.subscribe(TOPIC)
        while True:
            try:
                client.check_msg()
            except Exception as e:
                client = MQTTClient(client_id=TOPIC, server=SERVER, port=1883, keepalive=60)
                client.set_callback(mqtt_callback)
                client.connect()
                client.subscribe(TOPIC)
    except:
        machine.soft_reset()


if __name__ == '__main__':
    main()
