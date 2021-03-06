#!/usr/bin/env python3
#-*- coding: utf-8 -*-


import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import logging


#logging.basicConfig(filename='LOG/'+__name__+'.log',
#                    format='[%(asctime)s-%(filename)s-%(levelname)s: %(message)s]',
#                    level = logging.DEBUG,
#                    filemode='a')


# 发件人和收件人
sender = '422206217@leiqblog.top'


# 所使用的用来发送邮件的SMTP服务器
smtpserver = 'smtp.leiqblog.top'


# 发送邮箱的用户名和授权码（不是登录邮箱的密码）
username = '422206217@leiqblog.top'
password = '198653/a'


class send_email(object):
    def __init__(self, mail_title, mail_body, receiver=['422206217@qq.com']):
        self.mail_title = mail_title
        self.mail_body = mail_body
        self.receiver = receiver

    def do_send(self):
        # 邮件内容, 格式, 编码
        message = MIMEText(self.mail_body, 'html', 'utf-8')
        message['From'] = formataddr(["小胡子Haso", ""])
        message['To'] = formataddr(["神秘人", ""])
        message['Subject'] = Header(self.mail_title, 'utf-8')

        try:
            smtp=smtplib.SMTP()
            smtp.connect("smtp.leiqblog.top", 25)
            smtp.login(username, password)
            smtp.sendmail(sender, self.receiver, message.as_string())
            logging.info("发送邮件成功！！！")
            logging.info("发件人：" + str(message['From']) + "收件人：" + str(message['To']))
            smtp.quit()
        except smtplib.SMTPException:
            logging.error("发送邮件失败！！！")
