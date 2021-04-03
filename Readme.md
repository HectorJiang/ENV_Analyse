## Frist-Generation Architecture:

<img src="https://typora-markdown.oss-cn-shanghai.aliyuncs.com/img/image-20210102004730742.png" alt="image-20210102004730742" style="zoom: 67%;" width="300"/>

## Second-Generation Architecture:
on-going....

## Delopy with simple bash script


```
bash ./deploy.sh
```

```
#!/bin/bash
# Modify software source
echo "deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib" > /etc/apt/sources.list
echo "deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib" >> /etc/apt/sources.list
echo "deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui" > /etc/apt/sources.list.d/raspi.list
apt-get update

#
read -p "Please input hostname:" HOSTNAME
echo "$HOSTNAME" > /etc/hostname
hostname "$HOSTNAME"

#Install ufw firewall and open port necessary
apt-get install ufw -y
ufw allow 22/tcp
ufw allow 5000/tcp
ufw enable

#Install dependencies
apt-get install python3-pip libpcre3 libpcre3-dev -y
pip3 install -r requirements.txt

#Supporting BCM2711(tempature and humidty sensor is not supported by raspberrypi4) 
cp platform_detect.py /usr/local/lib/python3.7/dist-packages/Adafruit_DHT

# uwsgi start automaticly when pi boot.
cp start_uwsgi.sh /etc/init.d
update-rc.d start_uwsgi.sh defaults

# lstart uwsgi
uwsgi -d ./logs/uwsgi.log --ini ./config.ini

#register for master node
IP=`ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`
MAC=`cat /sys/class/net/wlan0/address`
read -p "Please Input master'IP:" MASTERIP
curl -v "http://${MASTERIP}:5000/register_node?hostname=${HOSTNAME}&ip=${IP}&mac=${MAC}"

```