import platform
import os
import sys

# return parameter:
#
# w: windows
# m: mac
# o: other system
#
###################

def systemJudge():
    if platform.system() == 'Windows':
        return 'w'
    elif platform.system() == 'Mac':
        return 'm'
    else:
        return 'o'

def getComputerInformation():
    info = platform.uname()

    Info = 'Your system:' + info[0] + '\n' + \
            'Computer name:' + info[1] + '\n' + \
            'Version: ' + info[2] + '\n' + \
            'System type:' + info[3] + '\n' + \
            'processor:' + info[4] + '\n' + \
            runPlace()

    return Info

def runPlace():
    return os.path.abspath(sys.argv[0])

