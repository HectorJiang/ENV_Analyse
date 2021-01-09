# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 2:24
# @Author  : Hector will
import time
import uuid
import json
from threading import Lock

import requests
from flask_login import login_required, logout_user, login_user
from flask import render_template, request, redirect, url_for,jsonify
from sqlalchemy import *
from app.libs.AlchemyEncoder import AlchemyEncoder
from app.models.data import Data, Node, User, db, Notice, Service
from flask import Blueprint
import datetime
from app import socketio
from app import cache


# 定义数据相关蓝图
core = Blueprint("core", __name__)
current_time = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")


@core.route("/register_node",methods=["GET"])
def register_node():
    hostname=request.args.get("hostname")
    ip=request.args.get("ip")
    mac=request.args.get("mac")
    print("节点:%s,IP地址为:%s,Mac地址为:%s=====正在注册..."%(hostname,ip,mac))
    info = "IP地址为:"+ ip + ",Mac地址为:"+ mac
    # db_node = Node.query.filter_by(ip=ip)
    # print(db_node)
    # if(db_node is None):
    node = Node(
        name=hostname,
        uid=uuid.uuid4().hex,
        mac=mac,
        ip=ip,
        status="0",
        remark="null",
        has_temp="",
        has_humd="",
        updated_at=current_time,
        created_at=current_time
    )
    db.session.add(node)
    # else:
    #     db_node.status="0"

    notice_data = Notice(
        uid=uuid.uuid4().hex,
        title="节点添加",
        status="0",  # 未读:0，已读:00
        rank="0",  # 警告：0，错误：00
        info=info,
    )
    db.session.add(notice_data)
    db.session.commit()
    # 发送邮箱通知
    from app.libs.email import email_send
    service=Service.query.filter_by(name="flask_mail邮件",).first()
    email_send(service,"节点添加:\n"+info)
    return "Register completed!!!"


thread = None
thread_lock = Lock()

# 监听客户端连接
@socketio.on('connect', namespace='/get_data')
def connect():
    print('客户端已经链接')
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_task)

# 启动异步线程发送数据
def background_task():
    while True:
        socketio.sleep(1)
        socketio.emit('connect',cache.get("data"),namespace='/get_data')

# 首页以及相关数据请求
@core.route("/",methods=["GET","POST"])
@login_required
def index():
    return render_template("index.html")


#定义首页单项记录
@core.route("/temp_node")
@login_required
def temp_node():
    try:
        node_list = Node.query.all()
    except Exception as e:
        print(e)
        return render_template("index.html")
    return render_template("temp_node.html", node_list=node_list)


# 定义温度传感器节点
@core.route("/temp_node_chart",methods=["GET","POST"])
@login_required
def temp_node_chart():
    ip = request.args.get('ip')
    if request.method == "POST":
        post_ip = request.values.get("ip")
        data = Data.query.order_by(desc("id")).filter_by(ip=post_ip).first()
        # 除false求平均值
        toprocess_data=[]
        toprocess_data.append(data.temp1)
        toprocess_data.append(data.temp2)
        toprocess_data.append(data.temp3)
        temp=remove_false(toprocess_data)
        return json.dumps({"created_at":str(data.created_at),"temp":temp})
    return render_template("temp_node_chart.html",ip=ip)


# 除去false求综合数据(温湿度综合与烟雾等综合)
def remove_false(data):
    if len(data)=="0":
        return false
    res=0
    count=0
    for i in data:
        if i is None:
            continue
        elif i=="false":
            continue
        elif i=="true":
            return "true"
        else:
           res=res+float(i)
           count=count+1
    if res==0:
        return "false"
    return res / count


# 首页湿度节点
@core.route("/humd_node")
@login_required
def humd_node():
    try:
        node_list = Node.query.all()
    except Exception as e:
        print(e)
        return render_template("index.html")
    return render_template("humd_node.html", node_list=node_list)


# 定义湿度传感器节点
@core.route("/humd_node_chart",methods=["GET","POST"])
@login_required
def humd_node_chart():
    ip = request.args.get('ip')
    if request.method == "POST":
        post_ip = request.values.get("ip")
        data = Data.query.order_by(desc("id")).filter_by(ip=post_ip).first()
        # 除false求平均值
        toprocess_data=[]
        toprocess_data.append(data.humd1)
        toprocess_data.append(data.humd2)
        toprocess_data.append(data.humd3)
        humd=remove_false(toprocess_data)
        return json.dumps({"created_at":str(data.created_at),"humd":humd})
    return render_template("humd_node_chart.html",ip=ip)


# 首页行人通过节点
@core.route("/people_node")
@login_required
def people_node():
    try:
        node_list = Node.query.all()
    except Exception as e:
        print(e)
        return render_template("index.html")
    return render_template("people_node.html", node_list=node_list)


# 定义people传感器节点
@core.route("/people_node_chart",methods=["GET","POST"])
@login_required
def people_node_chart():
    ip = request.args.get('ip')
    if request.method == "POST":
        post_ip = request.values.get("ip")
        data = Data.query.order_by(desc("id")).filter_by(ip=post_ip).first()
        # 除false求平均值
        toprocess_data=[]
        toprocess_data.append(data.people1)
        toprocess_data.append(data.people2)
        toprocess_data.append(data.people3)
        people=remove_false(toprocess_data)
        return json.dumps({"created_at":str(data.created_at),"people":people})
    return render_template("people_node_chart.html",ip=ip)


# 首页烟雾监测
@core.route("/smoke_node")
@login_required
def smoke_node():
    try:
        node_list = Node.query.all()
    except Exception as e:
        print(e)
        return render_template("index.html")
    return render_template("smoke_node.html", node_list=node_list)

# 定义smoke传感器节点
@core.route("/smoke_node_chart",methods=["GET","POST"])
@login_required
def smoke_node_chart():
    ip = request.args.get('ip')
    if request.method == "POST":
        post_ip = request.values.get("ip")
        data = Data.query.order_by(desc("id")).filter_by(ip=post_ip).first()
        # 除false求平均值
        toprocess_data=[]
        toprocess_data.append(data.smoke1)
        toprocess_data.append(data.smoke2)
        toprocess_data.append(data.smoke3)
        smoke=remove_false(toprocess_data)
        return json.dumps({"created_at":str(data.created_at),"smoke":smoke})
    return render_template("smoke_node_chart.html",ip=ip)


#定义节点列表
@core.route("/node_list",methods=["GET"])
@login_required
def node_list():
    page = request.args.get('page') or 1
    # paginate方法返回一个sqlalchemy.pagination类型对象
    node_list=Node.query.paginate(int(page),5)
    print(node_list)
    # node_list=Node.query.all()
    # print(node_list)
    tmp_time1 = (datetime.datetime.now() - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    tmp_time2 = (datetime.datetime.now() + datetime.timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    return render_template("node_list.html",pagination=node_list,node_list=node_list.items,updated_at=str(tmp_time1))



#定义节点数据
@core.route("/node_list_chart",methods=["POST","GET"])
@login_required
def node_list_chart():
    ip = request.args.get('ip')
    if request.method == "POST":
        post_ip = request.values.get("ip")
        data = Data.query.order_by(desc("id")).filter_by(ip=post_ip).first()
        # 除false求平均值
        toprocess_temp=[]
        toprocess_temp.append(data.temp1)
        toprocess_temp.append(data.temp2)
        toprocess_temp.append(data.temp3)
        toprocess_humd=[]
        toprocess_humd.append(data.humd1)
        toprocess_humd.append(data.humd2)
        toprocess_humd.append(data.humd3)
        toprocess_smoke=[]
        toprocess_smoke.append(data.smoke1)
        toprocess_smoke.append(data.smoke2)
        toprocess_smoke.append(data.smoke3)
        toprocess_people=[]
        toprocess_people.append(data.people1)
        toprocess_people.append(data.people2)
        toprocess_people.append(data.people3)
        toprocess_drop=[]
        toprocess_drop.append(data.drop1)
        toprocess_drop.append(data.drop2)
        toprocess_drop.append(data.drop3)
        # toprocess_current=[]
        # toprocess_current.append(data.current1)
        # toprocess_current.append(data.current2)
        # toprocess_current.append(data.current3)
        temp=remove_false(toprocess_temp)
        humd=remove_false(toprocess_humd)
        smoke=remove_false(toprocess_smoke)
        people=remove_false(toprocess_people)
        drop=remove_false(toprocess_drop)
        # current=remove_false(toprocess_current)
        return json.dumps({"created_at":str(data.created_at),"temp":temp,"humd":humd,"smoke":smoke,"people":people
                           ,"drop":drop,"current":""})
    return render_template("node_list_chart.html",ip=ip)


#定义节点查询
@core.route("/node_list_search")
@login_required
def node_list_search():
    ip = request.args.get('ip')
    mac = request.args.get('mac')
    try:
        if(len(ip)!=0 and len(mac)!=0 ):
            node_list = Node.query.filter_by(ip=ip,mac=mac).all()
        elif(len(ip)!=0 and len(mac)==0):
            node_list = Node.query.filter_by(ip=ip).all()
        elif(len(ip)==0 and len(mac)!=0):
            node_list = Node.query.filter_by(mac=mac).all()
        elif(len(ip)==0 and len(mac)==0):
            node_list=[]
    except Exception as e:
        print(e)
    return render_template("node_list_search.html",node_list=node_list)


# 单节点数据请求
@core.route("/node_data",methods=["GET","POST"])
@login_required
def node_data():
    if request.method=="POST":
        try:
            data=Data.query.order_by(desc("id")).filter_by(ip=node_addr).first()
        except Exception as e:
            return "出现一个错误"
        # 返回实时的综合数据

        return json.dumps(data,cls=AlchemyEncoder,ensure_ascii=False)

# 节点编辑
@core.route("/node_edit/<uid>",methods=["POST","GET"])
@login_required
def node_edit(uid):
    node=Node.query.filter_by(uid=uid).first()
    if request.method=="POST":
        request_data = request.form.to_dict()
        try:
            data = Node.query.filter_by(uid=request_data.get("uid")).first()
            data.name = request_data.get("name")
            data.remark = request_data.get("remark")
            db.session.commit()
            return redirect(url_for("core.node_list"))
        except Exception as e:
            print(e)
    return render_template("node_edit.html",node=node)


# 删除参数值
@core.route("/node_delete/<uid>")
def node_delete(uid):
    try:
        data = Node.query.filter_by(uid=uid).first()
        db.session.delete(data)
        db.session.commit()
        print("删除成功")
        return redirect(url_for("core.node_list"))
    except Exception as e:
        print(e)
        db.session.rollback()





# 历史数据查询（更新：以天定位，按照秒计算
@core.route("/get_history_data",methods=["POST","GET"])
@login_required
def get_history_data():
    if request.method=="POST":
        date=request.values.get("date")
        time1=request.values.get("time1")
        time2=request.values.get("time2")
        ip=request.values.get("ip")
        # 从前端表单中获取属性列表
        propertys=request.values.getlist("property")
        res=0
        if("temp" in propertys):
            res+=1
        if("humd" in propertys):
            res+=1
        if("people" in propertys):
            res+=1
        if("smoke" in propertys):
            res+=1
        if("drop" in propertys):
            res+=1
        print(res)
        # 遍历propertys中的值去查询数据库，然后将数据返回
        #
        # start_time=date+" "+time1
        # end_time=date+" "+time2
        # res=Data.query.filter(Data.ip==ip,Data.created_at >start_time,Data.created_at <end_time).all()
        # res=json.dumps(res, cls=AlchemyEncoder, ensure_ascii=False)
        # res=json.loads(res)
        print(propertys)

        data={}
        property_i=[]
        history_time=[]
        # 存储的json格式为:{"temp":{"temp1":[],"temp2":[]},"humd":{"humd1":[]},"history_time":[]}
        # 代码优化
        # for i in res:
        #     i_time = (str(i["created_at"]).split(" "))[1]
        #     history_time.append((i_time.split("."))[0])
        #     data["history_time"]=history_time
        #     for property in propertys:
        #         print(property)
        #         property_i.clear()
        #         for j in (1,2,3):
        #             tmp1=property+str(j)
        #             property_i.append(i[tmp1])
        #         data[property] = property_i
        #         print(property_i)
        #         print(data)
        #         # data[property] = property_i
        #         # print(data)



        # 2019-09-23 03:31:43.151754
        # 拼接字符串
        start_time=date+" "+time1
        end_time=date+" "+time2
        data=Data.query.filter(Data.ip==ip,Data.created_at >start_time,Data.created_at <end_time).all()
        #定义存储
        history_time=[]
        history_temp_data1=[]
        history_temp_data2=[]
        history_temp_data3=[]
        history_humd_data1=[]
        history_humd_data2 = []
        history_humd_data3 = []
        history_people_data1 = []
        history_people_data2 = []
        history_people_data3 = []
        history_drop_data1 = []
        history_drop_data2 = []
        history_drop_data3 = []
        history_current_data1 = []
        history_current_data2 = []
        history_current_data3 = []

        for i in data:
            i_time=(str(i.created_at).split(" "))[1]
            history_time.append((i_time.split("."))[0])
            history_temp_data1.append(i.temp1)
            history_temp_data2.append(i.temp2)
            history_temp_data3.append(i.temp3)
            history_humd_data1.append(i.humd1)
            history_humd_data2.append(i.humd2)
            history_humd_data3.append(i.humd3)
            history_people_data1.append(i.people1)
            history_people_data2.append(i.people2)
            history_people_data3.append(i.people3)
            history_drop_data1.append(i.drop1)
            history_drop_data2.append(i.drop2)
            history_drop_data3.append(i.drop3)
            # history_current_data1.append(i.current1)
            # history_current_data2.append(i.current2)
            # history_current_data3.append(i.current3)

        return render_template("history_data.html",history_time=history_time,history_temp_data1=history_temp_data1,history_temp_data2=history_temp_data2,
            history_temp_data3=history_temp_data3,history_humd_data1=history_humd_data1,history_humd_data2=history_humd_data2,history_humd_data3=history_humd_data3,
            history_people_data1=history_people_data1,history_people_data2=history_people_data2,
            history_people_data3=history_people_data3,history_drop_data1=history_drop_data1,
            history_drop_data2=history_drop_data2,history_drop_data3=history_drop_data3)
    return render_template("history_data.html")


# 系统通知
@core.route("/notice",methods=["POST","GET"])
@login_required
def notice():
    # data=Notice.query..order_by(desc("id")).all()
    page = request.args.get('page') or 1
    # paginate方法返回一个sqlalchemy.pagination类型对象
    notice=Notice.query.filter_by(status="0").order_by(desc("id")).paginate(int(page),5)
    return render_template("notice.html",pagination=notice)


# ajax实时请求系统通知数目
@core.route("/notice_count",methods=["POST","GET"])
@login_required
def notice_count():
    if request.method=="POST":
        count=Notice.query.filter_by(status="0").count()
        return jsonify({"count":count})



# 系统通知，标记已读
@core.route("/notice_read/<uid>")
@login_required
def notice_read(uid):
    try:
        notice = Notice.query.filter_by(uid=uid).first()
        notice.status="00"#标记为已读
        db.session.commit()
        print("修改成功")
    except Exception as e:
        print(e)
    return redirect(url_for("core.notice"))



# 系统通知，标记未读
@core.route("/notice_unread/<uid>")
@login_required
def notice_unread(uid):
    try:
        notice = Notice.query.filter_by(uid=uid).first()
        notice.status="0"#标记为已读
        db.session.commit()
        print("修改成功")
    except Exception as e:
        print(e)
    else:
        print("修改失败")
    return redirect(url_for("core.notice"))


# 系统通知：具体信息
@core.route("/notice_info/<uid>")
@login_required
def notice_info(uid):
    notice = Notice.query.filter_by(uid=uid).first()
    return render_template("notice_info.html",notice_info=notice)


# 系统通知：删除信息
@core.route("/notice_delete/<uid>")
@login_required
def notice_delete(uid):
    try:
        notice = Notice.query.filter_by(uid=uid).first()
        db.session.delete(notice)
        db.session.commit()
        print("删除成功")
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for("core.notice"))

# 系统通知：全部标记为已读
@core.route("/notice_allread")
@login_required
def notice_allread():
    try:
        notice = Notice.query.all()
        for n in notice:
            n.status="00"
        db.session.commit()
        print("修改成功")
    except Exception as e:
        print(e)
    else:
        print("修改失败")
    return redirect(url_for("core.notice"))


# 全局可视化
@core.route("/global_view")
@login_required
def global_view():
    return render_template("global_view.html")


# 系统报告
@core.route("/system_report")
@login_required
def system_report():
    return render_template("system_report.html")
