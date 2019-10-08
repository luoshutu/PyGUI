# -*- coding: utf-8 -*
'''
#---Project--------------: PM1200监护仪，通过串口获取设备PM1200
#------------------------: 上传的血氧、血压、心电、体温等数据，
#------------------------: 上位机进行数据展示、波形绘制与开关操作
#----------------------------------------------------------------
#---DocumentDescription--: 实现上位机的布局和部件属性设置
#----------------------------------------------------------------
#---CreateTime-----------: 2019.10.1
#---By-------------------: luoshutu
'''

import PM1200Parameter as PMPar
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtWidgets import QPushButton,QWidget,QApplication,QGridLayout,QListWidget,QMessageBox
from PyQt5.QtWidgets import QLineEdit,QLabel,QTextBrowser,QMenu,QMenuBar,QComboBox,QTextEdit,QSpinBox
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

class Ui_MainWindow(object):
    """docstring for Ui_MainWindow"""
    def __init__(self, MainWindow):
        
        MainWindow.setWindowTitle('PM1200 监护仪')
        MainWindow.resize(1080,720)
        MainWindow.setFont(QFont('Times New Roman',9))
        self.centralWid = QtGui.QWidget()
        MainWindow.setCentralWidget(self.centralWid)
        self.MainLayout = QtGui.QGridLayout()
        self.centralWid.setLayout(self.MainLayout)

        self.boxMessage = QMessageBox()

        #Widget窗口布局
        self.layoutWidget = QtGui.QGridLayout()
        self.MainLayout.addLayout(self.layoutWidget,0,1,2,2)

        self.pw1 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pw1,0,0)

        self.pwV1 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwV1,0,1)

        self.pw2 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pw2,1,0)

        self.pwV2 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwV2,1,1)

        self.pw3 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pw3,2,0)

        self.pwV3 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwV3,2,1)

        self.pwaVR = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwaVR,3,0)

        self.pwV4 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwV4,3,1)

        self.pwaVL = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwaVL,4,0)

        self.pwV5 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwV5,4,1)

        self.pwAVF = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwAVF,5,0)

        self.pwV6 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwV6,5,1)

        self.pwResp = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwResp,6,0)

        self.pwSPO2 = pg.PlotWidget()
        self.layoutWidget.addWidget(self.pwSPO2,6,1)

        #参数显示布局
        self.layoutValue = QtGui.QGridLayout()
        self.MainLayout.addLayout(self.layoutValue,0,0)

        self.labelSPO2 = QLabel(PMPar.measureValue[0][0])
        self.labelSPO2.setFixedSize(100,30)
        self.layoutValue.addWidget(self.labelSPO2,0,0)

        self.labelPR = QLabel(PMPar.measureValue[1][0])
        self.layoutValue.addWidget(self.labelPR,1,0)

        self.labelCuff = QLabel(PMPar.measureValue[2][0])
        self.layoutValue.addWidget(self.labelCuff,2,0)

        self.labelSys = QLabel(PMPar.measureValue[3][0])
        self.layoutValue.addWidget(self.labelSys,3,0)

        self.labelMean = QLabel(PMPar.measureValue[4][0])
        self.layoutValue.addWidget(self.labelMean,4,0)

        self.labelDia = QLabel(PMPar.measureValue[5][0])
        self.layoutValue.addWidget(self.labelDia,5,0)

        self.labelHR = QLabel(PMPar.measureValue[6][0])
        self.layoutValue.addWidget(self.labelHR,6,0)

        self.labelRR = QLabel(PMPar.measureValue[7][0])
        self.layoutValue.addWidget(self.labelRR,7,0)

        self.labelST = QLabel(PMPar.measureValue[8][0])
        self.layoutValue.addWidget(self.labelST,8,0)

        self.labelARR = QLabel(PMPar.measureValue[9][0])
        self.layoutValue.addWidget(self.labelARR,9,0)

        self.labelTemp1 = QLabel(PMPar.measureValue[10][0])
        self.layoutValue.addWidget(self.labelTemp1,10,0)

        #self.labelTemp2 = QLabel(PMPar.measureValue[11][0])
        #self.layoutValue.addWidget(self.labelTemp2,11,0)

        self.TextBrowserSPO2 = QTextBrowser()
        self.TextBrowserSPO2.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserSPO2,0,1)

        self.TextBrowserPR = QTextBrowser()
        self.TextBrowserPR.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserPR,1,1)

        self.TextBrowserCuff = QTextBrowser()
        self.TextBrowserCuff.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserCuff,2,1)

        self.TextBrowserSys = QTextBrowser()
        self.TextBrowserSys.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserSys,3,1)

        self.TextBrowserMean = QTextBrowser()
        self.TextBrowserMean.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserMean,4,1)

        self.TextBrowserDia = QTextBrowser()
        self.TextBrowserDia.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserDia,5,1)

        self.TextBrowserHR = QTextBrowser()
        self.TextBrowserHR.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserHR,6,1)

        self.TextBrowserRR = QTextBrowser()
        self.TextBrowserRR.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserRR,7,1)

        self.TextBrowserST = QTextBrowser()
        self.TextBrowserST.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserST,8,1)

        self.TextBrowserARR = QTextBrowser()
        self.TextBrowserARR.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserARR,9,1)

        self.TextBrowserTemp1 = QTextBrowser()
        self.TextBrowserTemp1.setFixedSize(140,30)
        self.layoutValue.addWidget(self.TextBrowserTemp1,10,1)

        #self.TextBrowserTemp2 = QTextBrowser()
        #self.TextBrowserTemp2.setFixedSize(140,30)
        #self.layoutValue.addWidget(self.TextBrowserTemp2,11,1)

        self.spacerOne = QtWidgets.QSpacerItem(188, 16, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layoutValue.addItem(self.spacerOne, 11, 0, 12, 2)

        #按键和参数选择
        self.layoutButtonAndPar = QtGui.QGridLayout()
        self.MainLayout.addLayout(self.layoutButtonAndPar,1,0)

        #参数选择
        self.layoutPar = QtGui.QGridLayout()
        self.layoutButtonAndPar.addLayout(self.layoutPar,0,0)

        self.btnSer = QPushButton('打开串口：')
        self.btnSer.setFixedSize(90,30)
        self.layoutPar.addWidget(self.btnSer,0,0)

        self.textEditSer = QTextEdit()
        self.textEditSer.setFixedSize(140,30)
        self.layoutPar.addWidget(self.textEditSer,0,1)

        self.labelAdjust = QLabel('Adjust:')
        self.layoutPar.addWidget(self.labelAdjust,1,0)

        self.comboAdjust = QComboBox()
        self.layoutPar.addWidget(self.comboAdjust,1,1)

        self.labelBloodPre = QLabel('血压测量模式:')
        self.layoutPar.addWidget(self.labelBloodPre,2,0)

        self.comboBPModel = QComboBox()
        self.layoutPar.addWidget(self.comboBPModel,2,1)

        self.labelBloodPre = QLabel('袖带预充气(mmHg):')
        self.layoutPar.addWidget(self.labelBloodPre,3,0)

        self.spinBoxBP = QSpinBox()
        self.layoutPar.addWidget(self.spinBoxBP,3,1)

        self.labelECG = QLabel('心电测量模式:')
        self.layoutPar.addWidget(self.labelECG,4,0)

        self.comboECGModel = QComboBox()
        self.layoutPar.addWidget(self.comboECGModel,4,1)

        self.labelECGGain = QLabel('心电波形增益:')
        self.layoutPar.addWidget(self.labelECGGain,5,0)

        self.comboECGGain = QComboBox()
        self.layoutPar.addWidget(self.comboECGGain,5,1)

        self.labelRespGain = QLabel('呼吸波形增益:')
        self.layoutPar.addWidget(self.labelRespGain,6,0)

        self.comboRespGain = QComboBox()
        self.layoutPar.addWidget(self.comboRespGain,6,1)

        #按键布局
        self.layoutButton = QtGui.QGridLayout()
        self.layoutButtonAndPar.addLayout(self.layoutButton,1,0)

        self.btnSPO2 = QPushButton('血氧(OFF)')
        self.btnSPO2.setFixedSize(80,30)
        self.layoutButton.addWidget(self.btnSPO2,0,0)

        self.btnTemp = QPushButton('体温(OFF)')
        self.btnTemp.setFixedSize(80,30)
        self.layoutButton.addWidget(self.btnTemp,0,1)

        self.btnBloodPre = QPushButton('血压(OFF)')
        self.btnBloodPre.setFixedSize(80,30)
        self.layoutButton.addWidget(self.btnBloodPre,0,2)

        self.btnECG = QPushButton('心电(OFF)')
        self.btnECG.setFixedSize(80,30)
        self.layoutButton.addWidget(self.btnECG,1,0)

        self.btnV6 = QPushButton('V6(ON)')
        self.btnV6.setFixedSize(80,30)
        self.layoutButton.addWidget(self.btnV6,1,1)

        self.btnResp = QPushButton('Resp(OFF)')
        self.btnResp.setFixedSize(80,30)
        self.layoutButton.addWidget(self.btnResp,1,2)

    #部件属性设置
    def SettingComponentProperties(self):
        self.textEditSer.setPlainText('/dev/ttyACM0')

        #pwSPO2.setLabel('left', 'Amplitude', units='')
        #pwSPO2.setLabel('bottom', 'Time', units='s')
        self.pwSPO2.setTitle('血氧波形')
        self.pwSPO2.setXRange(0, 200)
        self.pwSPO2.setYRange(0, 100)

        self.pw1.setTitle('心电波形1')
        self.pw1.setXRange(0, 1000)
        self.pw1.setYRange(0, 250)

        self.pw2.setTitle('心电波形2')
        self.pw2.setXRange(0, 1000)
        self.pw2.setYRange(0, 250)

        self.pw3.setTitle('心电波形3')
        self.pw3.setXRange(0, 1000)
        self.pw3.setYRange(0, 250)

        self.pwV1.setTitle('心电波形V1')
        self.pwV1.setXRange(0, 1000)
        self.pwV1.setYRange(0, 250)

        self.pwV2.setTitle('心电波形V2')
        self.pwV2.setXRange(0, 1000)
        self.pwV2.setYRange(0, 250)

        self.pwV3.setTitle('心电波形V3')
        self.pwV3.setXRange(0, 1000)
        self.pwV3.setYRange(0, 250)

        self.pwV4.setTitle('心电波形V4')
        self.pwV4.setXRange(0, 1000)
        self.pwV4.setYRange(0, 250)

        self.pwV5.setTitle('心电波形V5')
        self.pwV5.setXRange(0, 1000)
        self.pwV5.setYRange(0, 250)

        self.pwV6.setTitle('心电波形V6')
        self.pwV6.setXRange(0, 1000)
        self.pwV6.setYRange(0, 250)

        self.pwaVL.setTitle('心电波形aVL')
        self.pwaVL.setXRange(0, 1000)
        self.pwaVL.setYRange(0, 250)

        self.pwaVR.setTitle('心电波形aVR')
        self.pwaVR.setXRange(0, 1000)
        self.pwaVR.setYRange(0, 250)

        self.pwAVF.setTitle('心电波形aVF')
        self.pwAVF.setXRange(0, 1000)
        self.pwAVF.setYRange(0, 250)

        self.pwResp.setTitle('呼吸波形Resp')
        self.pwResp.setXRange(0, 800)
        self.pwResp.setYRange(0, 250)

        self.comboAdjust.addItem("静态压力校准")
        self.comboAdjust.addItem("静态压力偏差设置")
        self.comboAdjust.addItem("温度1偏差设置")
        self.comboAdjust.addItem("漏气检测")

        self.spinBoxBP.setMaximum(300)
        self.spinBoxBP.setValue(170)
        self.spinBoxBP.setMinimum(40)
        self.spinBoxBP.setSingleStep(10)

        self.comboBPModel.addItem("成人模式")
        self.comboBPModel.addItem("儿童模式")
        self.comboBPModel.addItem("新生儿模式")

        self.comboECGModel.addItem("手术模式")
        self.comboECGModel.addItem("监护模式")
        self.comboECGModel.addItem("诊断模式")
        self.comboECGModel.setCurrentIndex(1)

        self.comboECGGain.addItem("x0.25")
        self.comboECGGain.addItem("x0.5")
        self.comboECGGain.addItem("x1")
        self.comboECGGain.addItem("x2")
        self.comboECGGain.setCurrentIndex(2)

        self.comboRespGain.addItem("x0.25")
        self.comboRespGain.addItem("x0.5")
        self.comboRespGain.addItem("x1")
        self.comboRespGain.addItem("x2")
        self.comboRespGain.setCurrentIndex(2)
    #参数更新
    def TextBrowserUpdate(self):
        self.TextBrowserSPO2.setText(PMPar.measureValue[0][1])
        self.TextBrowserPR.setText(PMPar.measureValue[1][1])
        self.TextBrowserCuff.setText(PMPar.measureValue[2][1])
        self.TextBrowserSys.setText(PMPar.measureValue[3][1])
        self.TextBrowserMean.setText(PMPar.measureValue[4][1])
        self.TextBrowserDia.setText(PMPar.measureValue[5][1])
        self.TextBrowserHR.setText(PMPar.measureValue[6][1])
        self.TextBrowserRR.setText(PMPar.measureValue[7][1])
        self.TextBrowserST.setText(PMPar.measureValue[8][1])
        self.TextBrowserARR.setText(PMPar.measureValue[9][1])
        self.TextBrowserTemp1.setText(PMPar.measureValue[10][1])
        #self.TextBrowserTemp2.setText(PMPar.measureValue[11][1])

