# -*- coding: utf-8 -*
'''
#---Project--------------: PM1200监护仪，通过串口获取设备PM1200
#------------------------: 上传的血氧、血压、心电、体温等数据，
#------------------------: 上位机进行数据展示、波形绘制与开关操作
#----------------------------------------------------------------
#---DocumentDescription--: 实现串口的开关以及数据的读写
#----------------------------------------------------------------
#---CreateTime-----------: 2019.10.1
#---By-------------------: luoshutu
'''

import serial
import string
import binascii

portx       = 0       #串口端口号
bps         = 115200  #波特率
timeout     = None    #永远等待操作，0为立即返回请求结果，其他值为等待超时时间永远等待操作

COM         = 0       #串口
serReadFlag = False   #串口打开标志位

# 打开串口
def OpenPort():
    global COM
    flag = False
    try:
        COM = serial.Serial(portx, bps, timeout = timeout)
        #判断是否打开成功
        if(COM.is_open):
            flag = True
    except:
        flag = False
        print("串口打开异常")
    return flag

#写数据
def WriteData(text):
    global COM
    result = COM.write(bytes.fromhex(text))  # 写数据
    return result

#读数据
def ReadData():
    global COM,serReadFlag
    STRGLO = ""
    readData = ""
    #print("ReadData")
    if(serReadFlag):
        if COM.in_waiting:
            STRGLO = COM.read(COM.in_waiting)
            readData = str(binascii.b2a_hex(STRGLO))[2:-1]
            #print(readData)
    else:
        pass
        #print("串口未打开")
    return readData
