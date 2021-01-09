# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 2:25
# @Author  : Hector will
from flask_login import UserMixin

from app import db
from datetime import datetime


# 数据
class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    uid = db.Column(db.String(100), unique=True)  # 唯一标识
    ip = db.Column(db.String(100))  # ip地址
    temp1 = db.Column(db.String(100))
    temp2 = db.Column(db.String(100))
    temp3 = db.Column(db.String(100))
    humd1 = db.Column(db.String(100))
    humd2 = db.Column(db.String(100))
    humd3 = db.Column(db.String(100))
    smoke1 = db.Column(db.String(100))
    smoke2 = db.Column(db.String(100))
    smoke3 = db.Column(db.String(100))
    people1 = db.Column(db.String(100))
    people2 = db.Column(db.String(100))
    people3 = db.Column(db.String(100))
    drop1 = db.Column(db.String(100))
    drop2 = db.Column(db.String(100))
    drop3 = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 更新时间


    def __repr__(self):
        return "<Data %r>" % self.uid



# 节点列表
class Node(db.Model):
    __tablename__ = "node_list"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    uid = db.Column(db.String(100), unique=True)  # 唯一标识
    mac=db.Column(db.String(100))   # mac地址
    ip = db.Column(db.String(100))  # ip地址
    status = db.Column(db.String(100))  # 节点状态
    name = db.Column(db.String(100))  # 节点名称
    remark = db.Column(db.String(100))  # 节点备注
    has_temp = db.Column(db.String(100))  # 是否有温度传感器
    has_humd = db.Column(db.String(100))  # 是否有湿度传感器
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 更新时间


    def __repr__(self):
        return "<Node %r>" % self.uid


#用户
class User(db.Model, UserMixin):
    __tablename__="admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    uid = db.Column(db.String(100), unique=True)  # 唯一标识
    username = db.Column(db.String(100), unique=True)  # 用户名
    password=db.Column(db.String(100))  #密码
    status=db.Column(db.String(100))    #用户状态：等级，状态
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 更新时间

    def __repr__(self):
        return "<User %r>" % self.id


# 服务接口
class Service(db.Model):
    __tablename__="service"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    uid = db.Column(db.String(100), unique=True)  # 唯一标识
    name = db.Column(db.String(100), unique=True)  # 服务名称
    status=db.Column(db.String(100))    #服务状态：开关，正常，异常
    ref_link=db.Column(db.String(100))  #参考链接
    p1_key=db.Column(db.String(100))    #参数1
    p2_key=db.Column(db.String(100))    #参数2
    p3_key=db.Column(db.String(100))    #参数3
    p4_key=db.Column(db.String(100))    #参数4
    p5_key=db.Column(db.String(100))    #参数5
    p1_value=db.Column(db.String(100))    #参数1值
    p2_value=db.Column(db.String(100))    #参数2值
    p3_value=db.Column(db.String(100))    #参数3值
    p4_value=db.Column(db.String(100))    #参数4值
    p5_value=db.Column(db.String(100))    #参数5值  
    p1_description=db.Column(db.String(100))    #参数1描述
    p2_description=db.Column(db.String(100))    #参数2描述
    p3_description=db.Column(db.String(100))    #参数3描述
    p4_description=db.Column(db.String(100))    #参数4描述
    p5_description=db.Column(db.String(100))    #参数5描述      
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 更新时间

    def __repr__(self):
        return "<Service %r>" % self.id


# 定义系统环境变量，如预警
class System(db.Model):
    __tablename__="system_variable"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    uid = db.Column(db.String(100), unique=True)  # 唯一标识
    key = db.Column(db.String(100)) #变量名
    value=db.Column(db.String(100)) #变量值
    comment=db.Column(db.String(100)) #解释
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 更新时间

    def __repr__(self):
        return "<System %r>" % self.id


# 定义通知栏1
# 状态：已读，未读
# 等级：异常，警告
# 参数：参数名称，参数值，参数描述
#       参数描述：由插入数据生成：新增节点，传感器，，



# 如果参数值>预警值=》组合一条信息，发送；同时插入通知表
# 定义通知栏2
# 状态：已读，未读
# 等级：异常，警告
# 通知信息
# 通知时间
# 已读时间

class Notice(db.Model):
    __tablename__="notice"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    uid = db.Column(db.String(100), unique=True)  # 唯一标识
    status = db.Column(db.String(100)) #状态
    rank=db.Column(db.String(100)) #等级
    title=db.Column(db.String(100)) #通知标题
    info=db.Column(db.String(100)) #通知信息
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 通知时间
    updated_at = db.Column(db.DateTime, index=True, default=datetime.now)  # 已读时间

    def __repr__(self):
        return "<Notice %r>" % self.id