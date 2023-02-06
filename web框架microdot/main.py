import time

import network
from microdot import Microdot
import _thread

app = Microdot()
ssid = "忆享科技-1"
password = "yxkj@123"


def connectWifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    wlan.disconnect()
    wlan.connect(ssid, password)  # connect to an AP
    time.sleep(5)  # 等待几秒，要不然isconnected 一直是false
    if wlan.isconnected():
        print(wlan.ifconfig())  # get the interface's IP/netmask/gw/DNS addresses
    return wlan.isconnected()


def startAP():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid="esp32ap-test",authmode=network.AUTH_WPA_WPA2_PSK,password="123456789")
    print(wlan.ifconfig())


@app.route("/scan", methods=['GET'])
def index(request):
    wlan = network.WLAN(network.STA_IF)

    wifiList = wlan.scan()
    # for i in wifiList:
    #     print(i)
    return wifiList


def main():
    startAP()
    time.sleep(1)
    connectWifi(ssid=ssid, password=password)

    _thread.start_new_thread(app.run, ())
    # app.run()
    while True:
        time.sleep(10)


if __name__ == '__main__':
    main()
