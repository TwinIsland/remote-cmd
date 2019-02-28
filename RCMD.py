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

# ���� config
try:
   config = setConfig()
except BaseException:
   print('�������������ļ���')
   endProgram()

# ������������
if maillib.testMail(config):
   print("�������������������������")
else:
   print("����������������������ӣ���")
   endProgram()

# ask for input
mode = input("����ģʽ��1 ���Ǳ�����ģʽ��2\n> ")

if mode == "1":
    while True:
        # �����������ת��
        inp = maillib.encode64(bytes(input("control> "), encoding='utf-8'))

        try:
            # �����ʼ����� subject Ϊ"remote control system mail"
            maillib.sendMail(config, "remote control system mail", inp)
            print(": ���ͳɹ���")
        except BaseException:
            print(": δ�ܳɹ�ִ�з��ͣ�")
            input("�س�����...")

elif mode == "2":
    # ��ʼ��
    testStr = "Subject: remote control system mail"
    refreshFreq = config['RefreshWait']

    print("ִ�н�������Զ�̿���ϵͳ")
    print('�ѳɹ�����')

    # whether set nope
    if config['setNope'] == 1:
        time.sleep(2)
        runDir = sysdeter.runPlace()
        os.system('start nope.bat')
        os._exit(0)

    while True:
        try:
            # ˢ����
            time.sleep(refreshFreq)
            # ��ȡ��һ���ʼ�
            mail = maillib.getMail(config, 0)
            # �������ָ�� subject�����������ļ�
            if mail[6].decode() == testStr:
                # ����ʼ���Ϣ��ûʲô�ã�ֻ�ǿ������ܵ�
                print('\n')
                print(mail[0].decode())
                print(mail[3].decode())
                print(mail[6].decode())
                # �����ʼ�����ȡ����
                code = maillib.decode64(maillib.decode64(mail[-1])).decode()
                # ɾ�������ʼ�
                maillib.getMail(config, 1)
                # ���ͳɹ���־������
                if config['sendLogToMail'] == 1:
                    info = 'ִ������ɹ���ɣ�ָ�' + code
                    maillib.sendMail(config, 'mission Successful', info)
                # ִ������
                print("����ִ�е����" + code)
                os.system(code)
                print('\n')
        except BaseException:
            print('�������ʧȥ���ӣ����ڳ������³���')
            time.sleep(5)