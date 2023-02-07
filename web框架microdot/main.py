import json
import time
import network
from microdot import Microdot
import _thread

datas = {}


def initdata():
    global datas
    try:
        with open("data.bat", "r+", encoding="utf-8") as f:
            datas = json.loads(f.read())
    except:
        flush()
        with open("data.bat", "r+", encoding="utf-8") as f:
            datas = json.loads(f.read())


app = Microdot()


def flush():
    with open("data.bat", "w+", encoding="utf-8") as f:
        f.write(json.dumps(datas))


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
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    wlan.config(essid="esp32ap", authmode=network.AUTH_OPEN)
    # wlan.config(essid="esp32ap", channel=11, authmode=network.AUTH_WPA_WPA2_PSK, hidden=False, password="123456789")
    print(wlan.ifconfig())


def initCheck():
    initdata()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # activate the interface
    wlan.disconnect()
    wifiList = wlan.scan()
    result = False
    for i in wifiList:
        print(i[0].decode(), datas.keys())
        if i[0].decode() in datas.keys():
            result = connectWifi(ssid=i[0].decode(), password=datas[i[0].decode()])
            break
    return result


@app.route("/scan", methods=['GET'])
def scan(request):
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wifiList = wlan.scan()
    result = []
    for i in wifiList:
        print(i[0].decode())
        result.append(i[0].decode())
    return result


@app.route("/setwifi", methods=['GET'])
def setWifi(request):
    ssid = request.args.get('ssid')
    pwd = request.args.get('pwd')
    print(ssid, pwd)
    try:
        result = connectWifi(ssid=ssid, password=pwd)
        if result:
            datas[str(ssid)] = str(pwd)
            flush()
        return {"result": result}
    except Exception as e:
        return {"error": e}
    finally:
        app.shutdown()


def main():
    if initCheck() is False:
        time.sleep(1)
        startAP()
        # _thread.start_new_thread(app.run, ())
        app.run()
    time.sleep(1)
    print("连接WiFi")
    while True:
        time.sleep(10)


if __name__ == '__main__':
    main()
