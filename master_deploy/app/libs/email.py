from app import mail
from flask_mail import Message

# 发送邮件
def email_send(service,msg):
    msg = msg if msg else service.p2_value
    recipients = service.p3_value
    print(msg)
    message = Message(subject=service.p1_value, sender='2518183894@qq.com',recipients=[recipients], body=msg)
    try:
        mail.send(message)
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'