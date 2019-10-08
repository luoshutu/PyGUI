# -*- coding: utf-8 -*
'''
#---Project--------------: PM1200监护仪，通过串口获取设备PM1200
#------------------------: 上传的血氧、血压、心电、体温等数据，
#------------------------: 上位机进行数据展示、波形绘制与开关操作
#----------------------------------------------------------------
#---DocumentDescription--: 全局变量，下行控制数据以及窗口变量显示
#----------------------------------------------------------------
#---CreateTime-----------: 2019.10.1
#---By-------------------: luoshutu
'''

import numpy as np
import array

closeECG            = "55 AA 04 01 00 FA "  #关闭心电检测控制
closeBP             = "55 AA 04 02 00 F9 "  #关闭血压检测控制
closeSPO2           = "55 AA 04 03 00 F8 "  #关闭血氧检测控制
closeTemp           = "55 AA 04 04 00 F7 "  #关闭温度检测控制
closeECGWave        = "55 AA 04 FB 00 00 "  #关闭心电波形检测控制
closeSPO2Wave       = "55 AA 04 FE 00 FD "  #关闭血氧波形检测控制
closeRESWave        = "55 AA 04 FF 00 FC "  #关闭呼吸波形检测控制

openECG             = "55 AA 04 01 01 F9 "  #打开心电检测控制
openBP              = "55 AA 04 02 01 F8 "  #打开血压检测控制
openSPO2            = "55 AA 04 03 01 F7 "  #打开血氧检测控制
openTemp            = "55 AA 04 04 01 F6 "  #打开温度检测控制
openECGWave         = "55 AA 04 FB 01 FF "  #打开心电波形检测控制
openSPO2Wave        = "55 AA 04 FE 01 FC "  #打开血氧波形检测控制
openRESWave         = "55 AA 04 FF 01 FB "  #打开呼吸波形检测控制

bloodPreModelAdult  = "55 AA 04 09 01 F1 "  #血压测量的成人模式
bloodPreModelChild  = "55 AA 04 09 02 F0 "  #血压测量的儿童模式
bloodPreModelBaby   = "55 AA 04 09 03 EF "  #血压测量的新生儿模式

ECGModelOper        = "55 AA 04 08 01 F2 "  #心电测量手术模式
ECGModelCustody     = "55 AA 04 08 02 F1 "  #心电测量监护模式
ECGModelDiag        = "55 AA 04 08 03 F0 "  #心电测量监护模式

ECGGain025          = "55 AA 04 07 01 F3 "  #心电波形增益0.25倍
ECGGain05           = "55 AA 04 07 02 F2 "  #心电波形增益0.5倍
ECGGain1            = "55 AA 04 07 03 F1 "  #心电波形增益1倍
ECGGain2            = "55 AA 04 07 04 F0 "  #心电波形增益2倍

RespGain025         = "55 AA 04 0F 01 EB "  #呼吸波形增益0.25倍
RespGain05          = "55 AA 04 0F 02 EA "  #呼吸波形增益0.5倍
RespGain1           = "55 AA 04 0F 03 E9 "  #呼吸波形增益1倍
RespGain2           = "55 AA 04 0F 04 E8 "  #呼吸波形增益2倍

V6Wave              = "55 AA 04 F7 00 04 "  #V6波形输出
RespWave            = "55 AA 04 F7 01 03 "  #呼吸波形输出

measureValue = np.array([                   #参数表
    ('血氧饱和度'   , '未开启'),
    ('脉率'        , '未开启'),
    ('袖带压力'     , '未开启'),
    ('收缩压'       , '未开启'),
    ('平均压'       , '未开启'),
    ('舒张压'       , '未开启'),
    ('心率'         , '未开启'),
    ('呼吸率'       , '未开启'),
    ('ST电位(mV)'   , '未开启'),
    ('心律异常代码'  , '未开启'),
    ('体温'        , '未开启'),
    #('体温2'        , '未开启'),
    ], dtype=[('参数名', object),('参数值', object)])

