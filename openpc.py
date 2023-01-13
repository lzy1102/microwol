import socket
import pprint
import binascii

"""mac.txt的格式化为每行一个mac地址.如下任意形式的mac地址:
FFFFFFFFFFFF
44850004F4EE
00-FF-AC-C0-BB-CA
44-85-00-04-F4-EE
44:87:01:04:F4:EE
"""
f = lambda x: x.strip() if len(x.strip()) == 12 else x.strip().replace(x.strip()[2], "")
mac = [f(r) for r in open("mac.txt")]
print("目标MAC地址列表:")  # mac.txt中的mac地址会被处理成FFFFFFFFFFFF无分隔符紧揍形式
pprint.pprint(mac)
ip = "192.168.199.255"
port = 9
ps = "fsfafda"  # password
ps = ps.encode()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


def sendto(r):
    s.sendto(r, (ip, port))


# python利用or在列表解析中调用多个函数 http://www.cnblogs.com/gayhub/p/5277919.html
[print("正在向:", r, "施法!") or sendto(binascii.unhexlify('FF' * 6 + r * 16) + ps) for r in mac]
s.close()
input("打完收功,回车退出!")
# 2016年3月21日 19:54:36