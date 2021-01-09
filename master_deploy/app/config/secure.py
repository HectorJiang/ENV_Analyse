# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 2:26
# @Author  : Hector will
# 数据库，系统安全相关配置

SQLALCHEMY_DATABASE_URI= "mysql+cymysql://root:@localhost:3306/jf"  # 定义Mysql数据库连接
SECRET_KEY = '6a8312d499ed42828bb85fefac3607b7'  # CSRF保护设置密钥

SCHDULER_API_ENABLED=True