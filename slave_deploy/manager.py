from flask import Flask,request,jsonify
import json
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import socket
import fcntl
import struct
import requests
import json
import uuid

# 创建app
app = Flask(__name__)

# 获取mac地址
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])
# 获取主机名
def get_hostname():
    return socket.gethostname()
# 获取IP地址
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15],'utf-8')))[20:24])


# 初始化参数
sensor = Adafruit_DHT.DHT11
# 启用BCM模式
GPIO.setmode(GPIO.BCM)
ip = get_ip_address('wlan0')
mac = get_mac_address()
hostname = get_hostname()


# 只接受get方法访问
@app.route("/get_data",methods=["GET"])
def get_data():
    store_data = []
        # 针脚14,15,18用来读取温湿度
    for i in [14, 15, 18]:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if GPIO.input(i) == True:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, i)
        #     print(i)
        #     print('{0:0.1f}*C {1:0.1f}%'.format(temperature, humidity))
            store_data.append(str(humidity))
            store_data.append(str(temperature))
        else:
        #     print(i)
        #     print('Failed to get reading.')
            store_data.append('false')
            store_data.append('false')

    # 针脚23,24,25用来读取雨滴数据
    for i in [23, 24, 25]:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if GPIO.input(i) == True:
            # print("pin"+str(i)+"no rain")
            store_data.append('false')
        else:
            # print("pin"+str(i)+"rain")
            store_data.append('true')

    # 针脚8,7,1用来读取烟感数据
    for i in [8, 7, 1]:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if GPIO.input(i) == True:
            # print("pin"+str(i)+"smoke")
            store_data.append('true')
        else:
            # print("pin"+str(i)+"no smoke")
            store_data.append('false')

    # 针脚12,16,20用来读取行人数据
    for i in [12, 16, 20]:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if GPIO.input(i) == True:
            # print("pin"+str(i)+"detect people")
            store_data.append('true')
        else:
            # print("pin"+str(i)+"no people")
            store_data.append('false')
#     print(mac)
#     print(json.dumps(store_data, ensure_ascii=False))
    print(store_data)
    data = {'ip': ip, 'mac': mac, 'hostname':hostname,'detail': store_data}
    # print(data)
    return jsonify(data)
#     res=requests.post(url="http://192.168.43.76:5000/store_data",data=data)
#     print(res.text)
 
if __name__ == "__main__":
    app.run(host=ip)
