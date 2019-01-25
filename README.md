# 通过邮箱远程操控电脑

> 欢迎大家访问我的博客：[overfit blog](http://overfit.ml)
>
> 其实这个程序是我 1 年前写的，今天，在整理我之前写的代码时，突然找到了，在这篇博客里，我会分析一下这个小程序的实现步骤

![](https://overfit-photo-1257758577.cos.ap-guangzhou.myqcloud.com/2019/01/20/test.PNG)

## 我们的目的

用 python 做一个小程序，使得可以远程操控电脑，实现**关机，重启，打开网页..** 一系列的功能

## 分析

**远程：**有没有一种方法能够实现信息的交换，且不需要钱呢？当然有，那就是网上到处都可以找到的免费邮箱

**操控：**为了实现实现关机，重启，打开网页..一系列的功能，我们使用 windows 自带的 `cmd` 命令行，比如

```cmd
::1200秒后关机
shutdown -s -t 1200
::打开网页
start http://overfit.ml
::删除文件
del /f /im test.txt
::新建文件夹
md test
```

## 使用

python 3.6

## 程序文件

```fold
config.json ---> 配置文件
maillib.py ---> 接收、发送、处理邮件的库
远程cmd.py  ---> 主程序
```

## config.json

```txt
{
  "mailAccount" : "你的163邮箱@163.com",
  "mailPassword" : "你的密码",
  "RefreshWait" : 刷新频率（程序检查邮箱的频率，最好写5）
}
```

## maillib.py

> 里面包含了：发送邮件，删除邮件，获取第一封邮件的功能

```python
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
```

## 主程序 “远程cmd.py”

1. 导入必要的库

   ```python
   # encoding:gbk
   import json
   import maillib
   import os
   import time
   ```

2. 定义导入config.json的方程

   ```python
   # load the config
   def setConfig():
       configTxt = open('config.json',"r")
       return json.load(configTxt)
   ```

3. 定义如果程序出错后执行的代码

   ```python
   # end program code
   def endProgram():
       input()
       os._exit(0)
   ```

4. 设置 config

   ```python
   # 设置 config
   try:
       config = setConfig()
   except BaseException:
       print('不能载入配置文件！')
       endProgram()
   ```

5. 测试config里的mail能不能用

   ```python
   # 测试邮箱主机
   if maillib.testMail(config):
       print("主机与邮箱服务器连接正常！")
   else:
       print("不能与邮箱服务器构建链接！！")
       endProgram()
   ```

6. 询问执行的模式

   ```python
   # ask for input
   mode = input("控制模式：1 还是被控制模式：2\n> ")
   ```

7. 如果是控制端的话

   ```python
   if mode == "1":
   	while True:
           # 把输入加密且转码
           inp = maillib.encode64(bytes(input("> "),encoding='utf-8'))
   		
           try:
               # 发送邮件，并 subject 为"remote control system mail"
               maillib.sendMail(config,"remote control system mail",inp)
               print(": 发送成功！")
           except BaseException:
               print(": 未能成功执行发送！")
               input("回车重试...")
   ```

8. 如果是被控制端的话

   ```python
   elif mode == "2":
       # 初始化
       testStr = "Subject: remote control system mail"
       refreshFreq = config['RefreshWait']
   
       print("执行进入主机远程控制系统")
       print('已成功进入')
       while True:
           try:
               # 刷新率
               time.sleep(refreshFreq)
               # 获取第一封邮件
               mail = maillib.getMail(config,0)
               # 如果满足指定 subject，即有命令文件
               if mail[6].decode() == testStr:
                   # 输出邮件信息，没什么用，只是看起来很吊
                   print('\n')
                   print(mail[0].decode())
                   print(mail[3].decode())
                   print(mail[6].decode())
                   # 分析邮件，获取命令
                   code = maillib.decode64(maillib.decode64(mail[-1])).decode()
                   # 删除命令邮件
                   maillib.getMail(config,1)
                   # 发送成功日志到邮箱
                   info = '执行任务成功完成，指令：'+ code
                   maillib.sendMail(config,'mission Successful',info)
                   # 执行命令
                   print("正在执行的命令："+ code)
                   os.system(code)
                   print('\n')
           except BaseException:
               print('与服务器失去连接，正在尝试重新尝试')
               time.sleep(5)
   ```
