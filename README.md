# PyQt编写GUI
  ### Project     : 
    PM1200监护仪，通过串口获取设备PM1200上传的血氧、血压、心电、体温等数据，上位机进行数据展示、波形绘制与开关操作。
  ### CreateTime  : 
    2019.10.1
  ### By          : 
    luoshutu
    
  ### Description :
    其中PM1200.py文件为main文件，实现数据的校验、波形的更新以及槽函数。
    PM1200DataAnalysis.py实现数据的解析。
    PM120Layout.py实现上位机的布局和部件属性设置。
    PM1200Parameter.py全局变量，下行控制数据以及窗口变量显示。
    PM1200Serial.py实现串口的开关以及数据的读写。
    
  ### UpDateDescription :
    2019.10.1
    实现输入串口号后进行打开关闭操作。
    在打开串口之前，测量按钮点击无效。
    
    2019.10.8
    血压测量完成后自动改变血压按钮状态。
    串口错误的异常处理
  	
    2019.10.10
    添加心电导联状态显示。
    使用QtDesigner设计UI2019.10.14
    血氧波形显示延迟bug改正
    
