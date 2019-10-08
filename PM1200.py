# -*- coding: utf-8 -*
'''
#---Project--------------: PM1200监护仪，通过串口获取设备PM1200
#------------------------: 上传的血氧、血压、心电、体温等数据，
#------------------------: 上位机进行数据展示、波形绘制与开关操作
#----------------------------------------------------------------
#---DocumentDescription--: main文件，实现数据的解析、波形的更新
#------------------------: 以及槽函数
#----------------------------------------------------------------
#---CreateTime-----------: 2019.10.1
#---By-------------------: luoshutu
'''

import PM1200Layout as PMLayout
import PM1200Parameter as PMPar
import PM1200Serial as PMSer
import PM1200DataAnalysis as PMDA
import string
import array
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

ui                  = ''                    #用户界面

N                   = 1200                  #屏幕上显示的曲线长度

plotSPO2            = ''                    #血氧曲线
plotResp            = ''
plot1               = ''
plot2               = ''
plot3               = ''
plotV1              = ''
plotV2              = ''
plotV3              = ''
plotV4              = ''
plotV5              = ''
plotV6              = ''
plotaVR             = ''
plotaVF             = ''
plotaVL             = ''

SPO2Series          = array.array('d')      #可动态改变数组的大小，曲线值缓存
respSeries          = array.array('d')
series1             = array.array('d')
series2             = array.array('d')
series3             = array.array('d')
seriesV1            = array.array('d')
seriesV2            = array.array('d')
seriesV3            = array.array('d')
seriesV4            = array.array('d')
seriesV5            = array.array('d')
seriesV6            = array.array('d')
seriesaVL           = array.array('d')
seriesaVR           = array.array('d')
seriesaVF           = array.array('d')

#按键状态标志位
btnSPO2_flag        = False
btnBloodPre_flag    = False
btnECG_flag         = False
btnTemp_flag        = False
btnResp_flag        = False
btnV6_flag          = False
btnSer_flag         = False

#波形数据更新
def FigureShow(plotAm, series, plotSeries):
    global N
    if(len(series) < N):
        series.append(plotAm)
    else:
        series[:-1] = series[1:]
        series[-1] = plotAm
    plotSeries.setData(series)
    #print(plotAm)

#接收的数据解析
def DataDecoding():
    global btnBloodPre_flag
    Data = ""
    Data = PMSer.ReadData()
    if(len(Data) >= 8):                                                                         #数据应至少包含包头和包长度以及一个包数据共4个字节
        for i in range(len(Data) - 5):
            if(Data[0 + i] == '5' and Data[1 + i] == '5' and Data[2 + i] == 'a' and Data[3 + i] == 'a'):    #判断包头
                dataLength = int(Data[4 + i] + Data[5 + i], 16)                                 #每包数据的有效信息长度
                if((i + 4 + 2*dataLength) > len(Data)):
                    break
                #if(dataLength == (len(Data) - 4) / 2):                                         #判断包长度
                sumCheck = 0
                for j in range(dataLength - 1):                                                 #和校验数据计算所得和
                    sumCheck += int(Data[i + 2 * j + 4] + Data[i + 2 * j + 5], 16)
                    #print(2 * i+4,sumCheck)
                sumData = int(Data[i + 2 + 2*dataLength] + Data[i + 3 + 2*dataLength], 16)      #数据所带用于校验的和
                if(255 - (sumCheck % 256) == sumData):                                          #和校验
                    #判断数据属于哪一类的测量值
                    if(Data[6 + i] == '0' and Data[7 + i] == '1'):                              #心电波形
                        Amplitude1, Amplitude2, Amplitude3, \
                        AmplitudeaVR, AmplitudeaVL, AmplitudeaVF, \
                        AmplitudeV1 = PMDA.ECGWave1Decoding(Data[i:i+(4+2*dataLength)])
                        FigureShow(Amplitude1, series1, plot1)
                        FigureShow(Amplitude2, series2, plot2)
                        FigureShow(Amplitude3, series3, plot3)
                        FigureShow(AmplitudeaVR, seriesaVR, plotaVR)
                        FigureShow(AmplitudeaVL, seriesaVL, plotaVL)
                        FigureShow(AmplitudeaVF, seriesaVF, plotaVF)
                        FigureShow(AmplitudeV1, seriesV1, plotV1)
                    elif(Data[6 + i] == 'f' and Data[7 + i] == '7'):                            #心电波形
                        AmplitudeV2, AmplitudeV3, AmplitudeV4, AmplitudeV5, \
                        AmplitudeV6 = PMDA.ECGWave2Decoding(Data[i:i+(4+2*dataLength)])
                        FigureShow(AmplitudeV2, seriesV2, plotV2)
                        FigureShow(AmplitudeV3, seriesV3, plotV3)
                        FigureShow(AmplitudeV4, seriesV4, plotV4)
                        FigureShow(AmplitudeV5, seriesV5, plotV5)
                        FigureShow(AmplitudeV6, seriesV6, plotV6)
                    elif(Data[6 + i] == '0' and Data[7 + i] == '2'):                            #心电参数
                        PMDA.ECGDecoding(Data[i:i+(4+2*dataLength)])
                        ui.TextBrowserUpdate()
                    elif(Data[6 + i] == '0' and Data[7 + i] == '3'):                            #血压值
                        measureStatus = PMDA.BloodPreDecoding(Data[i:i+(4+2*dataLength)])
                        if(measureStatus):
                            PMSer.WriteData(PMPar.closeBP)
                            ui.btnBloodPre.setText('血压(OFF)')
                            btnBloodPre_flag = False
                        ui.TextBrowserUpdate()
                    elif(Data[6 + i] == '0' and Data[7 + i] == '4'):                            #血氧值
                        PMDA.SPO2Decoding(Data[i:i+(4+2*dataLength)])
                        ui.TextBrowserUpdate()
                    elif(Data[6 + i] == '0' and Data[7 + i] == '5'):                            #温度
                        PMDA.TempDecoding(Data[i:i+(4+2*dataLength)])
                        ui.TextBrowserUpdate()
                    elif(Data[6 + i] == 'f' and Data[7 + i] == 'e'):                            #血氧波形幅值
                        FigureShow(PMDA.SPO2WaveDecoding(Data[i:i+(4+2*dataLength)]),SPO2Series,plotSPO2)
                        #print("血氧波形数据")
                    elif(Data[6 + i] == 'f' and Data[7 + i] == 'f'):                            #呼吸波形幅值
                        FigureShow(PMDA.RespWaveDecoding(Data[i:i+(4+2*dataLength)]),respSeries,plotResp)
                else:
                    pass
                    #print("数据错误")
            else:
                pass
                #print("数据包头错误")
    else:
        pass
        #print("数据丢失")

#串口开关
def on_btnSer():
    global ui
    if(ui.btnSer.text() == '打开串口：'):
        PMSer.portx = ui.textEditSer.toPlainText()
        #print(portx)
        PMSer.serReadFlag = PMSer.OpenPort()
        if(PMSer.serReadFlag):
            ui.btnSer.setText('关闭串口：')
            print("串口已打开：", '\n', PMSer.COM)
            PMDA.CloseAll()
        else:
            print("串口打开失败")
            ui.boxMessage.setText("串口打开失败,请检查连接！")
            ui.boxMessage.show()
    else:
        PMSer.COM.close()
        print("串口已关闭")
        PMSer.serReadFlag = False
        ui.btnSer.setText('打开串口：')

#血氧按键，控制血氧采集开关
def on_btnSPO2():
    global btnSPO2_flag, ui
    if(PMSer.serReadFlag):
        btnSPO2_flag = ~btnSPO2_flag
        if(btnSPO2_flag):
            flag = PMSer.WriteData(PMPar.openSPO2 + PMPar.openSPO2Wave)
            if(flag):
                ui.btnSPO2.setText('血氧(ON)')
                PMPar.measureValue[0][1] = '正在初始化'
                PMPar.measureValue[1][1] = '正在初始化'
            else:
                ui.boxMessage.setText("打开失败！")
                ui.boxMessage.show()
                btnSPO2_flag = False
        else:
            PMSer.WriteData(PMPar.closeSPO2 + PMPar.closeSPO2Wave)
            PMPar.measureValue[0][1] = '未开启'
            PMPar.measureValue[1][1] = '未开启'
            ui.btnSPO2.setText('血氧(OFF)')
        ui.TextBrowserUpdate()
    else:
        ui.boxMessage.setText("请先打开串口！")
        ui.boxMessage.show()

#控制血压采集开关
def on_btnBloodPre():
    global btnBloodPre_flag, ui
    if(PMSer.serReadFlag):
        btnBloodPre_flag = ~btnBloodPre_flag
        if(btnBloodPre_flag):
            BPModel = ui.comboBPModel.currentIndex()
            if(BPModel == 0):
                PMSer.WriteData(PMPar.bloodPreModelAdult)
                print("血压测量的成人模式")
            elif(BPModel == 1):
                PMSer.WriteData(PMPar.bloodPreModelChild)
                print("血压测量的儿童模式")
            elif(BPModel == 2):
                PMSer.WriteData(PMPar.bloodPreModelBaby)
                print("血压测量的新生儿模式")
            cuffPressure = hex(int(ui.spinBoxBP.value() / 2))
            sumCheck = hex(255 - (14 + int(ui.spinBoxBP.value() / 2)))                                        #和校验数据计算所得和
            PMSer.WriteData('55 AA 04 0A ' + cuffPressure[2] + cuffPressure[3] + sumCheck[2] + sumCheck[3])   #设置预充气压力值
            PMSer.WriteData(PMPar.openBP)
            temp = '正在初始化'
            PMPar.measureValue[2][1] = temp
            PMPar.measureValue[3][1] = temp
            PMPar.measureValue[4][1] = temp
            PMPar.measureValue[5][1] = temp
            ui.btnBloodPre.setText('血压(ON)')
        else:
            PMSer.WriteData(PMPar.closeBP)
            temp = '测量终止'
            PMPar.measureValue[2][1] = temp
            PMPar.measureValue[3][1] = temp
            PMPar.measureValue[4][1] = temp
            PMPar.measureValue[5][1] = temp
            ui.btnBloodPre.setText('血压(OFF)')
        ui.TextBrowserUpdate()
    else:
        ui.boxMessage.setText("请先打开串口！")
        ui.boxMessage.show()

#控制温度采集
def on_btnTemp():
    global btnTemp_flag, ui
    if(PMSer.serReadFlag):
        btnTemp_flag = ~btnTemp_flag
        if(btnTemp_flag):
            PMSer.WriteData(PMPar.openTemp)
            temp = '正在初始化'
            PMPar.measureValue[10][1] = temp
            #PMPar.measureValue[11][1] = temp
            ui.btnTemp.setText('体温(ON)')
        else:
            PMSer.WriteData(PMPar.closeTemp)
            temp = '未开启'
            PMPar.measureValue[10][1] = temp
            #PMPar.measureValue[11][1] = temp
            ui.btnTemp.setText('体温(OFF)')
        ui.TextBrowserUpdate()
    else:
        ui.boxMessage.setText("请先打开串口！")
        ui.boxMessage.show()

#设置呼吸波形显示
def on_btnResp():
    global btnResp_flag, btnV6_flag, ui
    btnResp_flag = True
    if(btnResp_flag):
        PMSer.WriteData(PMPar.openRESWave + PMPar.RespWave)
        ui.btnResp.setText('Resp(ON)')
        ui.btnV6.setText('V6(OFF)')

#设置心电V6波形显示
def on_btnV6():
    global btnResp_flag, btnV6_flag, ui
    btnV6_flag = True
    if(btnV6_flag):
        PMSer.WriteData(PMPar.V6Wave + PMPar.closeRESWave)
        ui.btnResp.setText('Resp(OFF)')
        ui.btnV6.setText('V6(ON)')

#控制心电采集
def on_btnECG():
    global btnECG_flag, ui
    if(PMSer.serReadFlag):
        btnECG_flag = ~btnECG_flag
        if(btnECG_flag):
            flag = PMSer.WriteData(PMPar.openECG + PMPar.openECGWave)
            if(flag):
                #设置心电测量模式
                ECGModel = ui.comboECGModel.currentIndex()
                if(ECGModel == 0):
                    PMSer.WriteData(PMPar.ECGModelOper)
                elif(ECGModel == 1):
                    PMSer.WriteData(PMPar.ECGModelCustody)
                elif(ECGModel == 2):
                    PMSer.WriteData(PMPar.ECGModelDiag)

                #设置心电波形增益
                ECGGain = ui.comboECGGain.currentIndex()
                if(ECGGain == 0):
                    PMSer.WriteData(PMPar.ECGGain025)
                elif(ECGGain == 1):
                    PMSer.WriteData(PMPar.ECGGain05)
                elif(ECGGain == 2):
                    PMSer.WriteData(PMPar.ECGGain1)
                elif(ECGGain == 3):
                    PMSer.WriteData(PMPar.ECGGain2)

                #设置呼吸波形增益
                RespGain = ui.comboRespGain.currentIndex()
                if(RespGain == 0):
                    PMSer.WriteData(PMPar.RespGain025)
                elif(RespGain == 1):
                    PMSer.WriteData(PMPar.RespGain05)
                elif(RespGain == 2):
                    PMSer.WriteData(PMPar.RespGain1)
                elif(RespGain == 3):
                    PMSer.WriteData(PMPar.RespGain2)

                ui.btnECG.setText('心电(ON)')
                temp = '正在初始化'
                PMPar.measureValue[6][1] = temp
                PMPar.measureValue[7][1] = temp
                PMPar.measureValue[8][1] = temp
                PMPar.measureValue[9][1] = temp
            else:
                ui.boxMessage.setText("打开失败！")
                ui.boxMessage.show()
                btnECG_flag = False
        else:
            PMSer.WriteData(PMPar.closeECG + PMPar.closeECGWave + PMPar.closeRESWave)
            temp = '未开启'
            PMPar.measureValue[6][1] = temp
            PMPar.measureValue[7][1] = temp
            PMPar.measureValue[8][1] = temp
            PMPar.measureValue[9][1] = temp
            ui.btnECG.setText('心电(OFF)')
            #btnV6.setText('V6(OFF)')
        ui.TextBrowserUpdate()
    else:
        ui.boxMessage.setText("请先打开串口！")
        ui.boxMessage.show()

#血压测量模式选择
def on_comboBPModel():
    global ui
    BPModel = ui.comboBPModel.currentIndex()
    if(BPModel == 0):
        ui.spinBoxBP.setValue(170)
        ui.spinBoxBP.setMaximum(300)
        print("血压测量的成人模式")
    elif(BPModel == 1):
        ui.spinBoxBP.setValue(100)
        ui.spinBoxBP.setMaximum(210)
        print("血压测量的儿童模式")
    elif(BPModel == 2):
        ui.spinBoxBP.setValue(70)
        ui.spinBoxBP.setMaximum(140)
        print("血压测量的新生儿模式")

#心电测量模式选择
def on_comboECGModel():
    global ui
    ECGModel = ui.comboECGModel.currentIndex()
    print(PMSer.serReadFlag)
    if(True == PMSer.serReadFlag):
        if(ECGModel == 0):
            PMSer.WriteData(PMPar.ECGModelOper)
            print("心电测量的手术模式")
        elif(ECGModel == 1):
            PMSer.WriteData(PMPar.ECGModelCustody)
            print("心电测量的监护模式")
        elif(ECGModel == 2):
            PMSer.WriteData(PMPar.ECGModelDiag)
            print("心电测量的诊断模式")
    else:
        print("串口未打开")

#心电波形增益设置
def on_comboECGGain():
    global ui
    ECGGain = ui.comboECGGain.currentIndex()
    if(True == PMSer.serReadFlag):
        if(ECGGain == 0):
            PMSer.WriteData(PMPar.ECGGain025)
            print("心电波形增益0.25倍")
        elif(ECGGain == 1):
            PMSer.WriteData(PMPar.ECGGain05)
            print("心电波形增益0.5倍")
        elif(ECGGain == 2):
            PMSer.WriteData(PMPar.ECGGain1)
            print("心电波形增益1倍")
        elif(ECGGain == 3):
            PMSer.WriteData(PMPar.ECGGain2)
            print("心电波形增益2倍")
    else:
        print("串口未打开")

#呼吸波形增益设置
def on_comboRespGain():
    global ui
    RespGain = ui.comboRespGain.currentIndex()
    if(True == PMSer.serReadFlag):
        if(RespGain == 0):
            PMSer.WriteData(PMPar.RespGain025)
            print("呼吸波形增益0.25倍")
        elif(RespGain == 1):
            PMSer.WriteData(PMPar.RespGain05)
            print("呼吸波形增益0.5倍")
        elif(RespGain == 2):
            PMSer.WriteData(PMPar.RespGain1)
            print("呼吸波形增益1倍")
        elif(RespGain == 3):
            PMSer.WriteData(PMPar.RespGain2)
            print("呼吸波形增益2倍")
    else:
        print("串口未打开")

#信号与槽函数连接
def signalConnectSlot():
    global ui
    #button信号连接
    ui.btnSPO2.clicked.connect(on_btnSPO2)
    ui.btnBloodPre.clicked.connect(on_btnBloodPre)
    ui.btnSer.clicked.connect(on_btnSer)
    ui.btnTemp.clicked.connect(on_btnTemp)
    ui.btnECG.clicked.connect(on_btnECG)
    ui.btnResp.clicked.connect(on_btnResp)
    ui.btnV6.clicked.connect(on_btnV6)

    #comboBox信号连接
    ui.comboBPModel.currentIndexChanged.connect(on_comboBPModel)
    ui.comboECGModel.currentIndexChanged.connect(on_comboECGModel)
    ui.comboECGGain.currentIndexChanged.connect(on_comboECGGain)
    ui.comboRespGain.currentIndexChanged.connect(on_comboRespGain)

def plotSetting():
    global ui, plotSPO2, plotResp, plot1, plot2, plot3, plotaVR, plotV1
    global plotV2, plotV3, plotV4, plotV5, plotV6, plotaVF, plotaVL

    plotSPO2 = ui.pwSPO2.plot()
    plotSPO2.setPen((0,0,200))

    plotResp = ui.pwResp.plot()
    plotResp.setPen((0,0,200))

    plot1 = ui.pw1.plot()
    plot1.setPen((0,0,200))

    plot2 = ui.pw2.plot()
    plot2.setPen((0,0,200))

    plot3 = ui.pw3.plot()
    plot3.setPen((0,0,200))

    plotV1 = ui.pwV1.plot()
    plotV1.setPen((0,0,200))

    plotV2 = ui.pwV2.plot()
    plotV2.setPen((0,0,200))

    plotV3 = ui.pwV3.plot()
    plotV3.setPen((0,0,200))

    plotV4 = ui.pwV4.plot()
    plotV4.setPen((0,0,200))

    plotV5 = ui.pwV5.plot()
    plotV5.setPen((0,0,200))

    plotV6 = ui.pwV6.plot()
    plotV6.setPen((0,0,200))

    plotaVF = ui.pwAVF.plot()
    plotaVF.setPen((0,0,200))

    plotaVL = ui.pwaVL.plot()
    plotaVL.setPen((0,0,200))

    plotaVR = ui.pwaVR.plot()
    plotaVR.setPen((0,0,200))

def main():
    global ui

    #用户界面
    app = QtGui.QApplication([])
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    MainWindow = QtGui.QMainWindow()
    ui = PMLayout.Ui_MainWindow(MainWindow)

    ui.SettingComponentProperties()                     #设置ui的部件属性和参数
    ui.TextBrowserUpdate()                              #文本参数显示刷新
    signalConnectSlot()                                 #信号与槽函数连接
    plotSetting()                                       #绘图设置
    MainWindow.show()

    #定时读取串口数据
    timerReadData = QtCore.QTimer()
    timerReadData.timeout.connect(DataDecoding)
    timerReadData.start(1)

    app.exec_()

if __name__ == "__main__":
    main()

