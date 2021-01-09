#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:hectorwill
# datetime:2019/9/17 14:46
# file: message.py
# 短信相关配置

# 短信应用 SDK AppID
appid = 1400257144  # SDK AppID 以1400开头
# 短信应用 SDK AppKey
appkey = "c86d889b0991edef5345ab841369c125"
# 需要发送短信的手机号码
phone_numbers = ["15922334968"]
# 短信模板ID，需要在短信控制台中申请
template_id = 421862  # NOTE: 这里的模板 ID`7839`只是示例，真实的模板 ID 需要在短信控制台中申请
# 签名
sms_sign = "小小灯泡"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是示例，真实的签名需要在短信控制台中申请