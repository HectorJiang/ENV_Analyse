# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 2:07
# @Author  : Hector will

from app import create_app,socketio
app = create_app()
# 项目入口

if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",debug=True)
