#coding:utf-8
#@Time: 2019/9/18 5:11
#@author: Hector will
#file: form.py
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# 定义登录表单
class LoginForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    submit=SubmitField("登录")

