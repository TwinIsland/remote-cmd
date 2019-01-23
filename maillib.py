
# code by Wyatt
# 20190123
# version 1

import smtplib
from poplib import POP3
from email.mime.text import MIMEText
import base64

def sendMail(config,sub,msg):

    mailAccount = config['mailAccount']
    mailPassword = config['mailPassword']

    message = MIMEText(msg, 'plain', 'utf-8')
    message['Subject'] = sub
    message['From'] = "remote control system"

    server = smtplib.SMTP('smtp.163.com')
    server.login(mailAccount, mailPassword)
    server.sendmail(mailAccount, mailAccount, message.as_string())
    server.quit()

def getMail(config,delmail):

    mailAccount = config['mailAccount']
    mailPassword = config['mailPassword']

    p = POP3('pop.163.com')
    p.user(mailAccount)
    p.pass_(mailPassword)
    resp, mails, octets = p.list()
    index = len(mails)
    resp, lines, octets = p.retr(index)
    if delmail == 1:
        p.dele(index)
    return lines

def testMail(config):

    mailAccount = config['mailAccount']
    mailPassword = config['mailPassword']

    try:
        server = smtplib.SMTP('smtp.163.com')
        server.login(mailAccount, mailPassword)
        p = POP3('pop.163.com')
        p.user(mailAccount)
        p.pass_(mailPassword)
        p.list()
    except BaseException:
        return 0
    return 1

def decode64(content):
    return base64.b64decode(content)

def encode64(content):
    return base64.b64encode(content)

# RECIEVE [0] TIME[3] CONTENTP[-1]