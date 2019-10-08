# -*- coding: utf-8 -*
'''
#---Project--------------: PM1200监护仪，通过串口获取设备PM1200
#------------------------: 上传的血氧、血压、心电、体温等数据，
#------------------------: 上位机进行数据展示、波形绘制与开关操作
#----------------------------------------------------------------
#---DocumentDescription--: 实现数据的解析
#----------------------------------------------------------------
#---CreateTime-----------: 2019.10.1
#---By-------------------: luoshutu
'''

import PM1200Parameter as PMPar
import PM1200Serial as PMSer

def get_s16(val):
    if val < 128:
        return val
    else:
        return (val - 256)

#心电参数解析
def ECGDecoding(Data):
    statusECG = int(Data[8]+Data[9],16)
    model = statusECG & 0x03
    if(model == 0):
        print("正常")
        heartR = int(Data[10]+Data[11],16)
        respR  = int(Data[12]+Data[13],16)
        ST     = get_s16(int(Data[14]+Data[15], 16))
        PMPar.measureValue[6][1] = str(heartR)
        PMPar.measureValue[7][1] = str(respR)
        PMPar.measureValue[8][1] = str(ST)

        if(Data[16] == '0'):
            if(Data[17] == '0'):
                print("正在分析")
                PMPar.measureValue[9][1] = "正在分析"
            elif(Data[17] == '1'):
                print("正常")
                PMPar.measureValue[9][1] = "正常"
            elif(Data[17] == '2'):
                print("停搏")
                PMPar.measureValue[9][1] = "停搏"
            elif(Data[17] == '3'):
                print("室颤/室速")
                PMPar.measureValue[9][1] = "室颤/室速"
            elif(Data[17] == '4'):
                print("R ON T")
                PMPar.measureValue[9][1] = "R ON T"
            elif(Data[17] == '5'):
                print("多个室早")
                PMPar.measureValue[9][1] = "多个室早"
            elif(Data[17] == '6'):
                print("成对室早")
                PMPar.measureValue[9][1] = "成对室早"
            elif(Data[17] == '7'):
                print("单个室早")
                PMPar.measureValue[9][1] = "单个室早"
            elif(Data[17] == '8'):
                print("二联律")
                PMPar.measureValue[9][1] = "二联律"
            elif(Data[17] == '9'):
                print("三联律")
                PMPar.measureValue[9][1] = "三联律"
            elif(Data[17] == 'a'):
                print("心动过速")
                PMPar.measureValue[9][1] = "心动过速"
            elif(Data[17] == 'b'):
                print("心动过缓")
                PMPar.measureValue[9][1] = "心动过缓"
            elif(Data[17] == 'c'):
                print("漏搏")
                PMPar.measureValue[9][1] = "漏搏"
    else:
        if(model == 1):
            print("心电信号弱")
            temp = "心电信号弱"
        elif(model == 2 or model == 3):
            print("心电导联脱落")
            temp = "心电导联脱落"
        PMPar.measureValue[6][1] = temp
        PMPar.measureValue[7][1] = temp
        PMPar.measureValue[8][1] = temp
        PMPar.measureValue[9][1] = temp

#心电波形解析
def ECGWave1Decoding(Data):
    Amplitude1   = int(Data[8]  + Data[9],16)
    Amplitude2   = int(Data[10] + Data[11],16)
    Amplitude3   = int(Data[12] + Data[13],16)
    AmplitudeaVR = int(Data[14] + Data[15],16)
    AmplitudeaVL = int(Data[16] + Data[17],16)
    AmplitudeaVF = int(Data[18] + Data[19],16)
    AmplitudeV1  = int(Data[20] + Data[21],16)

    return Amplitude1, Amplitude2, Amplitude3, \
           AmplitudeaVR, AmplitudeaVL, AmplitudeaVF, AmplitudeV1

#心电波形解析
def ECGWave2Decoding(Data):
    AmplitudeV2 = int(Data[8]  + Data[9],16)
    AmplitudeV3 = int(Data[10] + Data[11],16)
    AmplitudeV4 = int(Data[12] + Data[13],16)
    AmplitudeV5 = int(Data[14] + Data[15],16)
    AmplitudeV6 = int(Data[16] + Data[17],16)

    return AmplitudeV2, AmplitudeV3, AmplitudeV4, AmplitudeV5, AmplitudeV6


#呼吸波形解析
def RespWaveDecoding(Data):
    RespAmplitude = int(Data[8] + Data[9], 16)
    #print(SPO2Amplitude)
    return RespAmplitude


#血氧参数解析
def SPO2Decoding(Data):
    if(Data[8] == '0'):
        if(Data[9] == '0'):
            spo2 = int(Data[10] + Data[11], 16)
            pulse = int(Data[12] + Data[13], 16)
            print("正常")
            print("血氧饱和度：", spo2)
            print("脉率：", pulse)
            PMPar.measureValue[0][1] = str(spo2)
            PMPar.measureValue[1][1] = str(pulse)
        elif(Data[9] == '1'):
            print("血氧探头脱落")
            PMPar.measureValue[0][1] = '血氧探头脱落'
            PMPar.measureValue[1][1] = '血氧探头脱落'
        elif(Data[9] == '2'):
            print("血氧指夹空")
            PMPar.measureValue[0][1] = '血氧指夹空'
            PMPar.measureValue[1][1] = '血氧指夹空'
        elif(Data[9] == '3'):
            print("正在搜索脉搏")
            PMPar.measureValue[0][1] = '正在搜索脉搏'
            PMPar.measureValue[1][1] = '正在搜索脉搏'
        elif(Data[9] == '4'):
            print("脉搏搜索时间过长")
            PMPar.measureValue[0][1] = '脉搏搜索时间过长'
            PMPar.measureValue[1][1] = '脉搏搜索时间过长'

#血氧波形数据的获取
def SPO2WaveDecoding(Data):
    SPO2Amplitude = int(Data[8] + Data[9], 16)
    #print(SPO2Amplitude)
    return SPO2Amplitude

#血压参数解析
def BloodPreDecoding(Data):
    statusBloodPre = int(Data[8]+Data[9],16)
    #print(statusBloodPre)
    model = statusBloodPre & 0x03
    if(model == 0):
        print("成人模式")
    elif(model == 1):
        print("儿童模式")
    elif(model == 2):
        print("新生儿模式")

    measureStatus = (statusBloodPre >> 2) & 0x0f
    if(measureStatus == 0):
        Cuff = 2*int(Data[10] + Data[11], 16)
        Sys = int(Data[12] + Data[13], 16)
        Mean = int(Data[14] + Data[15], 16)
        Dia = int(Data[16] + Data[17], 16)

        print("测量完成")
        print("袖带压力：", Cuff)
        print("收缩压：", Sys)
        print("平均压：", Mean)
        print("舒张压：", Dia)

        PMPar.measureValue[2][1] = str(Cuff)
        PMPar.measureValue[3][1] = str(Sys)
        PMPar.measureValue[4][1] = str(Mean)
        PMPar.measureValue[5][1] = str(Dia)
    elif(measureStatus == 2):
        print("测量终止")
    else:
        if(measureStatus == 1):
            print("正在测量")
            temp = '正在测量'
        elif(measureStatus == 3):
            print("过压保护")
            temp = '过压保护'
        elif(measureStatus == 4):
            print("袖带太松或未接")
            temp = '袖带太松或未接'
        elif(measureStatus == 5):
            print("测量时间过长")
            temp = '测量时间过长'
        elif(measureStatus == 6):
            print("测量出错")
            temp = '测量出错'
        elif(measureStatus == 7):
            print("测量中有干扰")
            temp = '测量中有干扰'
        elif(measureStatus == 8):
            print("测量超出范围")
            temp = '测量超出范围'
        elif(measureStatus == 9):
            print("正在初始化")
            temp = '正在初始化'
        elif(measureStatus == 10):
            print("初始化完成")
            temp = '初始化完成'

        PMPar.measureValue[2][1] = temp
        PMPar.measureValue[3][1] = temp
        PMPar.measureValue[4][1] = temp
        PMPar.measureValue[5][1] = temp
    if(measureStatus == 1 or measureStatus == 9 or measureStatus == 10):
        return False
    else:
        return True

#温度参数解析
def TempDecoding(Data):
    if(Data[8] == '0'):
        if(Data[9] == '0'):
            TempOneInt = int(Data[10] + Data[11], 16)
            TempOneDec = int(Data[12] + Data[13], 16)
            TempOne = str(TempOneInt) + '.' + str(TempOneDec)
            print("正常")
            print("体温：", TempOne, "摄氏度")
            PMPar.measureValue[10][1] = TempOne
        elif(Data[9] == '1'):
            print("体温探头脱落")
            PMPar.measureValue[10][1] = '体温探头脱落'

#关闭所有采集
def CloseAll():
    closeAllTrans = PMPar.closeECG + PMPar.closeBP + PMPar.closeSPO2 + PMPar.closeTemp 
    closeAllTrans = closeAllTrans + PMPar.closeECGWave + PMPar.closeSPO2Wave + PMPar.closeRESWave
    #print(closeAllTrans)
    PMSer.WriteData(closeAllTrans)
