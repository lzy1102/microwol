import network
import socket
import time
import ustruct
from urequests import urequests


def connectWifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    wlan.disconnect()
    wlan.connect(ssid, password)  # connect to an AP
    time.sleep(5)  # 等待几秒，要不然isconnected 一直是false
    if wlan.isconnected():
        print(wlan.ifconfig())  # get the interface's IP/netmask/gw/DNS addresses


def wake_up(mac='DC-4A-3E-78-3E-0A', broadcast="192.168.1.255", port=7):
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


def main():
    ssid = "test666"
    password = "123456789"
    mac = "E0-D5-5E-7D-B9-EA"
    broadcast = "192.168.3.255"  # 广播地址
    port = 7  # 7 或者 9
    api = "http://106.12.129.198:5000"
    key = "583a80ba213d9361891994488f7715e8"
    connectWifi(ssid=ssid, password=password)
    while True:
        time.sleep_ms(10000)
        try:
            resp = urequests.get(url=api + "/getstatus", params={"mac": mac, "key": key})
            if str(resp.status_code) != "200":
                continue
            if resp.text == "1":
                print("开机")
                wake_up(mac=mac, broadcast=broadcast, port=port)
                time.sleep_ms(10000)
                urequests.get(url=api + "/setstatus", params={"mac": mac, "key": key, "status": 0})
        except Exception as e:
            print("获取状态错误", e)


if __name__ == '__main__':
    main()
