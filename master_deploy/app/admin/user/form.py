#coding:utf-8
#@Time: 2019/9/18 5:11
#@author: Hector will
#file: form.py
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# 定义登录表单
class LoginForm(FlaskForm):
    username=StringField('username',validators=[DataRequired("用户名不能为空")])
    password=PasswordField('password',validators=[DataRequired("密码不能为空")])
    submit=SubmitField("登录")



# 添加用户
class UserAddForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    repassword=PasswordField('repassword',validators=[DataRequired()])
    submit=SubmitField("确定")



# 修改用户密码
class UserProfileForm(FlaskForm):
    oldpassword=StringField('oldpassword',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    repassword=PasswordField('repassword',validators=[DataRequired()])
    submit=SubmitField("确定")