import network
import socket
import _thread
import time
from machine import Pin, Timer
import btree
import ustruct
from urequests import urequests
import wifimgr  # 这个模块名称务必要与上述WiFiManager模块文件名一致

# wlan = wifimgr.get_connection()
# if wlan is None:
#     print("Could not initialize the network connection.")
#     while True:
#         pass  # you shall not pass :D
#
#
# # Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
# print("ESP OK")

LED_BLINK = True


def led():
    p2 = Pin(12, Pin.OUT)
    p3 = Pin(13, Pin.OUT)
    while True:
        if not LED_BLINK:
            p2.off()
            p3.off()
            time.sleep(1000)
            continue
        p2.on()
        p3.off()
        time.sleep_ms(500)
        p2.off()
        p3.on()
        time.sleep_ms(500)


def serverWifi():
    # wlan = wifimgr.get_connection()
    # if wlan is None:
    #     print("Could not initialize the network connection.")
    #     while True:
    #         pass  # you shall not pass :D
    print("启动wifi server")
    ap = network.WLAN(network.AP_IF)  # create access-point interface
    ap.config(essid='ESP-AP', authmode=network.AUTH_WPA_WPA2_PSK, channel=11, password="123456789",
              max_clients=10)  # set the SSID of the access point
    ap.active(True)  # activate the interface
    print("启动wifi server 完成", ap.ifconfig())


def connectWifi():
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    wlan.disconnect()
    wlan.connect('yangdabao', 'lizhiyong418')  # connect to an AP
    time.sleep(5)
    if wlan.isconnected():
        print(wlan.ifconfig())  # get the interface's IP/netmask/gw/DNS addresses


def wake_up(mac='DC-4A-3E-78-3E-0A'):
    MAC = mac
    BROADCAST = "192.168.3.255"
    if len(MAC) != 17:
        raise ValueError("MAC address should be set as form 'XX-XX-XX-XX-XX-XX'")
    mac_address = MAC.replace("-", '')
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
        sock.sendto(send_data, (BROADCAST, 9))
        time.sleep(1)
        sock.sendto(send_data, (BROADCAST, 9))
        time.sleep(1)
        sock.sendto(send_data, (BROADCAST, 9))
        sock.close()
        print("Done")
    except Exception as e:

        print(e)


def main():
    global LED_BLINK
    print('----所有线程开始执行----')
    # serverWifi()
    # 创建互斥锁
    gLock = _thread.allocate_lock()
    # 获得互斥锁
    gLock.acquire()
    # 创建线程 点亮led灯
    _thread.start_new_thread(led, ())
    # 休眠
    time.sleep(5)
    # 释放互斥锁
    gLock.release()
    print('----主程序正在执行----')
    connectWifi()
    while True:
        time.sleep_ms(20000)
        print("循环开始")
        try:
            resp = urequests.get("http://106.12.129.198:5000/get")
            print(resp.status_code)
            if str(resp.status_code) != "200":
                continue
            if resp.text == "1":
                LED_BLINK=True
                print("开机")
                wake_up(mac="E0-D5-5E-7D-B9-EA")
                time.sleep_ms(5000)
                urequests.get("http://106.12.129.198:5000/set?status=0")
        except Exception as e:
            print("获取状态错误", e)
        LED_BLINK=False


if __name__ == '__main__':
    main()
