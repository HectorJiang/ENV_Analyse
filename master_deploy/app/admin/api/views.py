# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 2:24
# @Author  : Hector will
import uuid
import json

from flask_login import login_required, logout_user, login_user

from app.admin import api
from flask import render_template, request, redirect, url_for
from app import mail, login_manager
from flask_mail import Message
from app.config import message
from app.models.data import Service,db,System
from app.admin.api.form import SystemAddForm

from flask import Blueprint
# 定义数据相关蓝图

api = Blueprint("api", __name__)

# 定义服务接口
@api.route("/service")
@login_required
def service():
    try:
        service_list=Service.query.all()
    except Exception as e:
        print(e)
    return render_template("service_list.html",service_list=service_list);


# 定义服务开关接口
@api.route("/service_toggle",methods=["POST"])
@login_required
def service_toggle():
    if request.method=="POST":
        uid = request.values.get("uid")
        service=Service.query.filter_by(uid=uid).first()
        if service.status=="00":
            service.status="0"
        elif service.status=="0":
            service.status="00"
        db.session.commit()
        print(uid)
        return "ok"



# 发送短信预警，读取数据库参数
@api.route("/message",methods=["GET","POST"])
@login_required
def send_message():
    from qcloudsms_py import SmsSingleSender
    from qcloudsms_py.httpclient import HTTPError
    ssender = SmsSingleSender(message.appid, message.appkey)
    params = ["5678"]  # 当模板没有参数时，`params = []`
    try:
        result = ssender.send_with_param(86, message.phone_numbers[0],message.template_id, params, sign=message.sms_sign, extend="", ext="")
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    return render_template("index.html")







# api服务详细信息
@api.route("/service_info_edit",methods=["POST","GET"])
def service_info_edit():
    p=request.form.to_dict()
    if request.method=="POST":
        try:
            service=Service.query.filter_by(uid=p.get("uid")).first()
            service.p1_key=p.get("p1_key")
            service.p2_key=p.get("p2_key")
            service.p3_key=p.get("p3_key")
            service.p4_key=p.get("p4_key")
            service.p5_key=p.get("p5_key")
            service.p1_value=p.get("p1_value")
            service.p2_value=p.get("p2_value")
            service.p3_value=p.get("p3_value")
            service.p4_value=p.get("p4_value")
            service.p5_value=p.get("p5_value")
            service.p1_description=p.get("p1_description")
            service.p2_description=p.get("p2_description")
            service.p3_description=p.get("p3_description")
            service.p4_description=p.get("p4_description")
            service.p5_description=p.get("p5_description")
            db.session.commit()
            return redirect(url_for("api.service"))
        except Exception as e:
            print(e)
    return render_template("service_list.html")
# api服务详细信息
@api.route("/service_info/<uid>")
def service_info(uid):
    p=Service.query.filter_by(uid=uid).first()
    return render_template("service_info.html",p=p)



# 系统异常参数设置列表
@api.route("/service_set",methods=["POST","GET"])
def service_set():
    form=SystemAddForm()
    if form.validate_on_submit():
        key=form.key.data
        value=form.value.data
        comment=form.comment.data
        try:
            newvar=System(uid=uuid.uuid4().hex,key=key,value=value,comment=comment)
            db.session.add(newvar)
            db.session.commit()
            print("添加成功")
            return redirect(url_for("api.service_set"))
        except Exception as e:
            db.session.rollback()
            print(e)
    # 列表
    try:
        var=System.query.all()
    except Exception as e:
        print(e)
    return render_template("service_set.html",var_list=var,form=form)



# 系统参数设置详细信息
@api.route("/service_set_info/<uid>",methods=["GET","POST"])
def service_set_info(uid):
    var=System.query.filter_by(uid=uid).first()
    if request.method=="POST":
        pass
    return render_template("service_set_info.html",var=var)

# 修改参数值
@api.route("/service_set_edit",methods=["POST","GET"])
def service_set_edit():
    var=request.form.to_dict()
    try:
        db_var=System.query.filter_by(uid=var.get("uid")).first()
        db_var.key=var.get("key")
        db_var.value=var.get("value")
        db_var.comment=var.get("comment")
        db.session.commit()
        return redirect(url_for("api.service_set"))
    except Exception as e:
        print(e)


# 删除参数值
@api.route("/service_set_delete/<uid>")
def service_set_delete(uid):
    try:
        var = System.query.filter_by(uid=uid).first()
        db.session.delete(var)
        db.session.commit()
        print("删除成功")
        return redirect(url_for("api.service_set"))
    except Exception as e:
        print(e)
        db.session.rollback()

# 监听数据异常
# 方案一：设置定时任务，每秒查询数据库



