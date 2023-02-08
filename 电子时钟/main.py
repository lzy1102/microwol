#!/usr/bin/env python
# Created by iFantastic on 2023/2/8
import time
import ntptime
import utime
import network
from machine import Timer, Pin, RTC
import machine

ssid = "******"
password = "****"
led1 = Pin(12, Pin.OUT)


def connectWifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    wlan.disconnect()
    wlan.connect(ssid, password)  # connect to an AP
    time.sleep(5)  # 等待几秒，要不然isconnected 一直是false
    if wlan.isconnected():
        print(wlan.ifconfig())  # get the interface's IP/netmask/gw/DNS addresses
    return wlan.isconnected()


# 定时器回调，同步时间
def handler_callback(timer):
    # led1.value(not led1.value())
    sync_ntp()


# 获取网络时间，时间同步
def sync_ntp():
    try:
        print("同步前本地时间：%s" % str(time.localtime()))
        ntptime.NTP_DELTA = 3155644800  # 设置  UTC+8偏移时间（秒），不设置就是UTC0
        ntptime.host = 'time.windows.com'  # 可选ntp服务器为阿里云服务器，默认是"pool.ntp.org"
        ntptime.settime()  # 修改设备时间,到这就已经设置好了
        print("同步后本地时间：%s" % str(time.localtime()))
        return True
    except:
        print("同步出错")
        return False


def getTimestamp():
    return time.time() + 946656000 + 28800


def getTimeStr():
    tupleTime = time.gmtime(time.time() + 28800)
    # print(tupleTime)
    weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekday[tupleTime[6]], "{}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2}".format(tupleTime[0], tupleTime[1],
                                                                                 tupleTime[2],
                                                                                 tupleTime[3], tupleTime[4],
                                                                                 tupleTime[5])


def main():
    if not connectWifi(ssid=ssid, password=password):
        exit(1)
    tim = Timer(0)
    # 每小时同步一次
    tim.init(period=1000*60*60, mode=Timer.PERIODIC, callback=handler_callback)
    if not sync_ntp():
        machine.soft_reset()
    while True:
        t = getTimeStr()
        print(t[0], t[1])
        time.sleep(1)


if __name__ == '__main__':
    main()
