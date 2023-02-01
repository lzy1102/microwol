# microwol

main.py 是需要上传到板子上的程序，主要配置有以下几项

```python
ssid = "test666"   # 自己家的wifi名字，要和台式机在同一网段
password = "123456789"  #自家wifi密码
mac = "E0-D5-5E-7D-B9-EA"  #台式机MAC地址
broadcast = "192.168.3.255"  # 路由广播地址
port = 7  # 7 或者 9
api = "http://106.12.129.198:5000"  # 如果自己搭建服务器，换成自己的，如果不自己搭建，可以用我得
key = "583a80ba213d9361891994488f7715e8"  # 从服务获取到的key
```

key的获取方法如下

http://106.12.129.198:5000/getkey?mac=xxxxxxx

将mac地址替换成自己的mac即可

获取到key后，替换main.py的key

开机直接浏览器请求 

http://106.12.129.198:5000/setstatus?mac=xxxxxxxxx&key=388888888888888888845&status=1

status=1的时候执行开机，开机后会自动设置成0

搭配向日葵，就可以随时随地对家里的电脑进行开机，并远程了

