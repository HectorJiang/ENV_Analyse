import datetime
import json
import uuid
from threading import Thread
from app import cache
from app.config.threadconfig import insert_data_lock
from app.models.data import Node, System, Service, db, Data, Notice
from app import scheduler
import requests
from app.libs import systeminfo
from app.libs.email import email_send

def store_data():
    # 获取本地缓存数据,节点列表,预警参数,警告方式
    node_list,benchmark=get_cachedata()
    data_list = []
    data={}
    # 轮询节点获取数据,判断节点是否异常，cache存储每个节点无数据的次数，当20秒内达到10次就被认定为异常
    for node in node_list:
        key = cache.get(node) if cache.get(node) != None else 0
        try:
            url = "http://" + node + ":5000/get_data"
            res = requests.get(url, timeout=(3, 3))
            res = json.loads(res.text)
            data[res["ip"]]=res["detail"]
            data_list.append(res)
            # 判断节点数据是否超过阈值
            temp = float(res["detail"][1])
            humd = float(res["detail"][0])
            service = get_service()
            if(temp>=float(benchmark["temp"])):
                info = res["ip"] + "温度数据异常"
                Thread(target=notice, args=(service,info)).start()
            if(humd>=float(benchmark["humd"])):
                info = res["ip"] + "湿度数据异常"
                Thread(target=notice, args=(service,info)).start()
        except Exception as e:
            cache.set(node,key+1)
    # 启动多线程插入mysql
    Thread(target=insert_data,args=(data_list,)).start()
    # 将最新获取的数据加入缓存中,前端websocket接入传入数据
    data["systeminfo"] = get_systeminfo()
    print(data)
    # 查询系统通知数
    data["count"] = notice_count()
    cache.set("data",data,0)


# 查询系统通知数
def notice_count():
    with scheduler.app.app_context():
        count=Notice.query.filter_by(status="0").count()
        return count

# 获取系统实时信息
def get_systeminfo():
    public_ip = systeminfo.get_public_ip()
    private_ip = systeminfo.get_private_ip()
    mac = systeminfo.get_mac()
    disk = systeminfo.get_disk()
    memory = systeminfo.get_memory()
    cpu = systeminfo.get_cpu()
    return {"mac":mac,"public_ip":public_ip,"private_ip":private_ip,"disk":disk,"memory":memory,"cpu":cpu}


# 多线程插入最新数据
def insert_data(data_list):
    current_time = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    with scheduler.app.app_context():
        for data in data_list:
            data = Data(
                ip=data['ip'],
                uid=data['mac'],
                temp1=data['detail'][1],
                temp2=data['detail'][3],
                temp3=data['detail'][5],
                humd1=data['detail'][0],
                humd2=data['detail'][2],
                humd3=data['detail'][4],
                drop1=data['detail'][6],
                drop2=data['detail'][7],
                drop3=data['detail'][8],
                people1=data['detail'][9],
                people2=data['detail'][10],
                people3=data['detail'][11],
                smoke1=data['detail'][12],
                smoke2=data['detail'][13],
                smoke3=data['detail'][14],
                updated_at=current_time,
                created_at=current_time
            )
            # 加上线程同步锁
            insert_data_lock.acquire()
            try:
                db.session.add(data)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            insert_data_lock.release()

# 多线程发送警告
def notice(service,info):
    with scheduler.app.app_context():
        notice_data = Notice(
            uid=uuid.uuid4().hex,
            title="数据异常",
            status="0",  # 未读:0，已读:00
            rank="2",  # 0为插入,1为脱离,2为数据异常
            info=info,
        )
        db.session.add(notice_data)
        db.session.commit()
        # 发送邮箱通知
        email_send(service, "数据异常:\n" + info)


# 获取节点列表：将节点列表存入本地缓存当中，每20s从mysql中更新一次缓存
# 获取预警参数：将预警参数存入本地缓存当中，每20s从mysql中更新一次缓存
# 获取警告方式：将警告方式入本地缓存当中，每20s从mysql中更新一次缓存
# 设置函数缓存时间
@cache.cached(timeout=20, key_prefix='get_cachedata')
def get_cachedata():
    with scheduler.app.app_context():
        # 获取mysql数据
        node_list = []
        for node in Node.query.filter_by(status="0"):
            node_list.append(node.ip)
        benchmark = {}
        for param in System.query.all():
            benchmark[param.key] = param.value
        return node_list,benchmark

@cache.cached(timeout=20,key_prefix='get_service')
def get_service():
    with scheduler.app.app_context():
        service = Service.query.filter_by(name="flask_mail邮件", ).first()
        return service
# 判断节点是否脱离
def is_out():
    with scheduler.app.app_context():
        node_list,benchmark=get_cachedata()
        for node in node_list:
            if(cache.get(node) is not None and cache.get(node)> 10):
                # 通知栏
                info = "节点"+node+"脱离."
                notice_data = Notice(
                    uid=uuid.uuid4().hex,
                    title="节点脱离",
                    status="0",  # 未读:0，已读:00
                    rank="1",  # 警告：0，错误：00
                    info=info,
                )

                # 修改节点状态
                db_node = Node.query.filter_by(ip=node).first()
                db_node.status = "1"

                db.session.add(notice_data)
                db.session.commit()

                # 启动异步线程发送邮箱通知
                service = Service.query.filter_by(name="flask_mail邮件",).first()
                email_send(service,"节点脱离:\n" + info)
                print("%s节点出现异常"%node)
                # 清空记录
                cache.set(node,0)
            else:
                # 20秒内脱离次数小于10,缓存清0
                cache.set(node,0)








