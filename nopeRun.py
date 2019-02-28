# encoding:gbk
import json
import maillib
import time
import os

def setConfig():
    configTxt = open('config.json', "r")
    return json.load(configTxt)


config = setConfig()
# 初始化
testStr = "Subject: remote control system mail"
refreshFreq = config['RefreshWait']

if maillib.testMail(config):
    os.system('mshta vbscript:msgbox("已成功接入邮箱服务器，点击”确定“继续",64,"成功")(window.close)')
    while True:
        try:
            # 刷新率
            time.sleep(refreshFreq)
            # 获取第一封邮件
            mail = maillib.getMail(config, 0)
            # 如果满足指定 subject，即有命令文件
            if mail[6].decode() == testStr:
                # 分析邮件，获取命令
                code = maillib.decode64(maillib.decode64(mail[-1])).decode()
                # 删除命令邮件
                maillib.getMail(config, 1)
                # 发送成功日志到邮箱
                if config['sendLogToMail'] == 1:
                    info = '执行任务成功完成，指令：' + code
                    maillib.sendMail(config, 'mission Successful', info)
                os.system(code)
        except BaseException:
            time.sleep(5)
os.system('mshta vbscript:msgbox("接入失败！请检查config文件",64,"错误")(window.close)')