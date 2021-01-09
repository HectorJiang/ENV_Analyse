# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 2:07
# @Author  : Hector will
from functools import wraps

from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from flask_caching import Cache

# 注册蓝图
def register_blueprints(app):
    from app.admin.core.views import core as core_blueprint
    from app.admin.user.views import user as user_blueprint
    from app.admin.api.views import api as api_blueprint
    # from app.admin.warn.views import warn as warn_blueprint
    app.register_blueprint(core_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(api_blueprint)
    # app.register_blueprint(warn_blueprint)

cache = Cache()
db = SQLAlchemy()  #创建db对象
mail = Mail()      #创建mail对象
login_manager = LoginManager()  #创建登录对象

async_mode = None     # 新添加的代码
socketio = SocketIO()   # 新添加的代码


class Scheduler(APScheduler):
    """
    修改为单例模式，解决出现启动flask时，任务被执行两次的问题。
    """
    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        :param args:
        :param kwargs:
        :return:
        """
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
scheduler = Scheduler()


# 创建一个app对象
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.mail')

    # 导入定时任务配置类
    from app.config.JobConfig import JobConfig
    app.config.from_object(JobConfig)

    # 注册蓝图
    register_blueprints(app)
    # 数据库对象，邮箱对象绑定蓝图
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    cache.init_app(app,config={'CACHE_TYPE': 'filesystem','CACHE_DIR':'./app/cache'})
    # 初始化Flask-APScheduler，定时任务
    scheduler.init_app(app)
    scheduler.start()
    socketio.init_app(app=app,async_mode=async_mode,cors_allowed_origins="*")
    return app


# def sqlalchemy_context(app):
#     def add_context(func):
#         @wraps(func)
#         def do_job(*args, **kwargs):
#             app.app_context().push()
#             result = func(*args,**kwargs)
#             return result
#         return do_job
#     return add_context




