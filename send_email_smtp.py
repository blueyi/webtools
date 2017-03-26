#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ubuntu <ubuntu@dev>
#
# Distributed under terms of the MIT license.

"""

"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email import encoders
from email.utils import formatdate
from getpass import getpass
from os.path import basename
import time
import sys


def prompt(msg):
    return raw_input(msg).strip()


def curTimeStr():
    return time.strftime('%Y%m%d%H%M%S')

class SendMail:
    def __init__(self):
        self.smtp_server = None
        self.smtp_port = None
        self.user = None
        self.password = None
        self.subject = None
        self.html_content = None
        self.attachments = []
        self.to_list = []
        self.to_cc = []
        self.failed_list = []


    def send(self, mail_to):
        '''
        Send email through SMTP
        '''
        try:
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.login(self.user, self.password)
            server.sendmail(self.user, mail_to, self.msg_attachments(mail_to))
            server.close()
            print(mail_to + ' Success')
            return True
        except smtplib.SMTPException, e:
            print(e)
            return False


    def batch_send(self):
        for receiver in self.to_list:
            if not self.send(receiver):
                self.failed_list.append(receiver)
            time.sleep(180)
        if len(self.failed_list) != 0:
            print('Send Failed({}): '.format(len(self.failed_list)))
            print(self.failed_list)
            with open('failed_list_' + curTimeStr() + '.log', 'w') as f:
                f.write('\n'.join(self.failed_list))


    def msg_attachments(self, mail_to):
        # create html email
        emailMsg = MIMEMultipart('mixed')
        emailMsg['Subject'] = self.subject
        emailMsg['From'] = self.user
        emailMsg['Date'] = formatdate(localtime=True)
        emailMsg['To'] = ''
        if isinstance(mail_to, list):
            emailMsg['To'] = ', '.join(mail_to)
        elif isinstance(mail_to, str):
            emailMsg['To'] = mail_to
        emailMsg.attach(MIMEText(self.html_content, 'html'))

        # attach a file
        fileMsg = None
        if len(self.attachments) != 0:
            for file in self.attachments:
                with open(file, 'rb') as fp:
                    fileMsg = MIMEApplication(fp.read(), Name=basename(file))
                fileMsg.add_header('Content-Disposition', 'attachment; filename="%s"' % basename(file))
                emailMsg.attach(fileMsg)
        return emailMsg.as_string()


if __name__ == '__main__':
    user = ''
    password = ''
    email_list_file = ''
    email_list = []
    if len(sys.argv) < 4:
        user = prompt('User Name:')
        password = getpass('Password:')
        email_list_file = prompt('Email list file name:')
    else:
        user = sys.argv[1]
        password = sys.argv[2]
        email_list_file = sys.argv[3]

    fp = open(email_list_file, 'r')
    email_list = fp.read().splitlines()
    fp.close()
    qqmail = SendMail()
    qqmail.smtp_server = 'smtp.exmail.qq.com'
    qqmail.smtp_port = 465
    qqmail.user = user
    qqmail.password = password
    qqmail.subject = 'Getworld.in通知'
    qqmail.attachments = []
    qqmail.to_list = email_list
    qqmail.to_cc = []
    qqmail.failed_list = []
    qqmail.html_content = """\
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
            <body>
                <p>
                <a href="http://ss.getworld.in">ss.getworld.in</a>网站持续遭到攻击数月，由于近期增加了自动屏蔽攻击IP功能，
                有人通过QQ群举报将本群封停，已经重建新群：497034204。<br>
                近期将调整Getworld.in的节点，将停用“GetWorld-gmail-1”节点，并增加速度更快的“Getworld-美国节点-4”。<br>
                QQ群将增加准入限制，收集到的攻击IP已基本能确定攻击人个人信息，请攻击者自重！<br>
                再次重申：<h1>Getworld.in提供免费稳定的SS服务，请仅用于科学研究和学习之用，切勿它用!</h1><br>
                有任何问题可直接回复本邮件。<br>
                Ps:这些维护工作和节点，除了现金之外，花费了我大量的时间和精力，请珍惜！<br>
                <h2>Try to make the world a better place!</h2><br><br><br>
                ---powered by GetWorld.in Group
                </p>
            </body>
        </html>
        """
    qqmail.batch_send()