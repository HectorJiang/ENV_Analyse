#coding:utf-8
#@Time: 2019/9/18 5:11
#@author: Hector will
#file: form.py
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired



# 添加系统异常参数
class SystemAddForm(FlaskForm):
    key=StringField('key',validators=[DataRequired()])
    value=StringField('value',validators=[DataRequired()])
    comment=StringField('comment',validators=[DataRequired()])
    submit=SubmitField("确定")

