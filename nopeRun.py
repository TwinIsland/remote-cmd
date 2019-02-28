# encoding:gbk
import json
import maillib
import time
import os

def setConfig():
    configTxt = open('config.json', "r")
    return json.load(configTxt)


config = setConfig()
# ��ʼ��
testStr = "Subject: remote control system mail"
refreshFreq = config['RefreshWait']

if maillib.testMail(config):
    os.system('mshta vbscript:msgbox("�ѳɹ���������������������ȷ��������",64,"�ɹ�")(window.close)')
    while True:
        try:
            # ˢ����
            time.sleep(refreshFreq)
            # ��ȡ��һ���ʼ�
            mail = maillib.getMail(config, 0)
            # �������ָ�� subject�����������ļ�
            if mail[6].decode() == testStr:
                # �����ʼ�����ȡ����
                code = maillib.decode64(maillib.decode64(mail[-1])).decode()
                # ɾ�������ʼ�
                maillib.getMail(config, 1)
                # ���ͳɹ���־������
                if config['sendLogToMail'] == 1:
                    info = 'ִ������ɹ���ɣ�ָ�' + code
                    maillib.sendMail(config, 'mission Successful', info)
                os.system(code)
        except BaseException:
            time.sleep(5)
os.system('mshta vbscript:msgbox("����ʧ�ܣ�����config�ļ�",64,"����")(window.close)')