## 系统介绍

<img src="D:\Img\image-20210102004730742.png" alt="image-20210102004730742" style="zoom: 67%;" />



## 子节点与父节点部署

通过启动shell脚本一键部署

```
bash ./deploy.sh
```

```
#!/bin/bash
# 修改软件源
echo "deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib" > /etc/apt/sources.list
echo "deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib" >> /etc/apt/sources.list
echo "deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui" > /etc/apt/sources.list.d/raspi.list
apt-get update

#修改主机名
read -p "请输入主机名:" HOSTNAME
echo "$HOSTNAME" > /etc/hostname
hostname "$HOSTNAME"

#安装ufw防火墙，开放端口
apt-get install ufw -y
ufw allow 22/tcp
ufw allow 5000/tcp
ufw enable

#安装相关依赖并启动程序
apt-get install python3-pip libpcre3 libpcre3-dev -y
pip3 install -r requirements.txt

# 由于温湿度传感器不支持最新的树莓派4，BCM2711，自动添加支持
cp platform_detect.py /usr/local/lib/python3.7/dist-packages/Adafruit_DHT

# 设置开机启动uwsgi服务器
cp start_uwsgi.sh /etc/init.d
update-rc.d start_uwsgi.sh defaults

# 启动uwsgi服务器
uwsgi -d ./logs/uwsgi.log --ini ./config.ini

#向主节点注册信息
#获取本机IP地址和Mac地址
IP=`ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`
MAC=`cat /sys/class/net/wlan0/address`
read -p "请输入主节点IP地址:" MASTERIP
curl -v "http://${MASTERIP}:5000/register_node?hostname=${HOSTNAME}&ip=${IP}&mac=${MAC}"

```



1.启动主节点，部署服务器

2.启动子节点通过shell自动部署（安装相关依赖，向父节点自助注册）