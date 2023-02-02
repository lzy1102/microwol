# microwol

main.py 是需要上传到板子上的程序，主要配置有以下几项

```python
SERVER = 'broker.emqx.io'  # mqtt 服务器地址
TOPIC = '0622306f5a6a39ed99441934f532c8e1'.encode()   # 服务器获取到的key,mqtt的topic地址
ssid = "test666"    # 自家wifi地址
password = "123456789"  # 自家wifi 密码
```

key的获取方法如下

http://106.12.129.198:5000/getkey

将mac地址替换成自己的mac即可

获取到key后，替换main.py的key

开机直接浏览器请求 

http://106.12.129.198:5000/setstatus?mac=40-E2-30-B1-31-E5&key=xxxxxxxxxxxxxxxx&broadcast=192.168.3.255&port=7

```python
mac = 'xxxxx'  # 自己要开机的电脑的mac地址
key  # 获取到的key
broadcast # 自家路由器的广播地址  192.168.3.255
port  # 电脑上魔法包的接受地址 通常是 9 或者 7
```

搭配向日葵，就可以随时随地对家里的电脑进行开机，并远程了

