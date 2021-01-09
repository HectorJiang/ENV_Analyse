#!/bin/bash
#设置开机自动启动
uwsgi -d ./logs/uwsgi.log --ini ./config.ini
