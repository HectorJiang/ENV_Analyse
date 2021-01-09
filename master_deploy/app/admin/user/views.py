# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 2:24
# @Author  : Hector will
from flask_login import login_required, logout_user, login_user,current_user
from app.admin import user
from flask import render_template, request, redirect, url_for,session
from app import mail, login_manager
from app.admin.core.form import LoginForm
from app.admin.user.form import UserAddForm, UserProfileForm
from app.models.data import Data, Node, User,db,Notice
from flask import Blueprint
import uuid
import time
# 定义数据相关蓝图
user = Blueprint("user", __name__)


# 定义flask_login中用户加载
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# 定义未授权跳转视图
# login_manager.login_view = "user.login"
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("user.login"))



#定义登录视图
@user.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        try:
            user=User.query.filter_by(username=username).first()
            if user is not None and user.password==password:
                print("登录成功")
                # 更新上次登录时间
                user.updated_at=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                db.session.commit()
                login_user(user)
                # 全局通知未读消息
                # notice = Notice.query.filter_by(status="0").count()
                # session['notice']=notice
                return redirect(url_for('core.index'))
            else:
                print("登录失败")
        except Exception as e:
            print(e)

    return render_template("login.html",form=form)



# 定义用户列表，添加用户
@user.route("/user_list",methods=["POST","GET"])
def user_list():
    # 添加用户表单请求
    form=UserAddForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        repassword=form.repassword.data
        try:
            user=User.query.filter_by(username=username).first()
            print(user)
            if user is None and password==repassword:
                newuser=User(uid=uuid.uuid4().hex,username=username,password=password,status=0)
                db.session.add(newuser)
                db.session.commit()
                print("添加成功")
                return redirect(url_for("user.user_list"))
            else:
                print("添加失败")
        except Exception as e:
            db.session.rollback()
            print(e)

    # 普通用户列表
    try:
        user_list=User.query.filter_by(status=0).all()
        print(user_list)
    except Exception as e:
        print(e)
    return render_template("user_list.html",user_list=user_list,form=form)


# 定义修改密码
@user.route("/user_profile",methods=["GET","POST"])
@login_required
def user_profile():
    form=UserProfileForm()
    oldpassword=form.oldpassword.data
    password=form.password.data
    repassword=form.repassword.data
    try:
        user = User.query.filter_by(uid=current_user.uid).first()
        if oldpassword==user.password and password==repassword:
            user.password=password
            db.session.commit()
            print("修改成功")
    except Exception as e:
        print(e)
    else:
        print("修改失败")
    return render_template("user_profile.html",form=form)


# 定义删除用户
@user.route("/user_delete/<uid>")
@login_required
def user_delete(uid):
    try:
        user = User.query.filter_by(uid=uid).first()
        db.session.delete(user)
        db.session.commit()
        print("删除成功")
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for("user.user_list"))


#定义退出
@user.route("/user_logout")
@login_required
def user_logout():
    logout_user()
    return redirect(url_for("user.login"))

