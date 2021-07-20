# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'untitled.ui'
# Created by: PyQt5 UI code generator 5.9.2
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets,QtWebEngineWidgets
import io,sys,folium
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import numpy as np
import json
import pickle
import requests
from geopy.distance import geodesic
path=r'C:\Users\34780\Desktop\大二下\数据结构\作业\city-geo-master\data.json'
def dis(point1,point2):
    return geodesic((point1[0],point1[1]),(point2[0],point2[1])).m
def geocodeG(address):
    KEY = '07ac12a00f830764ebfdee2fd0bc96fd'
    par = {'address': address, 'key': KEY}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, par)
    answer = response.json()
    if answer['count']=='0':
       return None
    else:
       return answer
class Route:
    def __init__(self):
        self.type=""
        self.x=[]
        self.y=[]
        self.note=[]
        self.route=[]
        self.dis=0
        self.o=""
        self.d=""
        self.time=0
def Way(approach,o,d):
    print(o,d)

    def stepWay(o, d):
        KEY = '07ac12a00f830764ebfdee2fd0bc96fd'
        origin, destination = geocodeG(o)['geocodes'][0]['location'], geocodeG(d)['geocodes'][0]['location']
        if origin == None or destination == None:
            print("No stepWay")
            return None, None, None
        route = Route()
        route.o, route.d = o, d
        OUTPUT = 'json'
        url = 'https://restapi.amap.com/v3/direction/walking?parameters'
        params = {'origin': origin, 'destination': destination, 'key': KEY, 'output': OUTPUT}
        output = json.loads(requests.get(url, params).content)
        if output['status'] == '0' or output['count'] == 0:
            print("No Step Way")
            return None, None, None
        else:
            data = output['route']['paths'][0]['steps']
            route.type = "step"
            route.dis = output['route']['paths'][0]['distance']
            route.time = output['route']['paths'][0]['duration']
            for li in data:
                route.note.append(li['instruction'])
                temp = li['polyline'].split(';')
                for k in temp:
                    k = k.split(',')
                    route.x.append(float(k[1]))
                    route.y.append(float(k[0]))
            route.route = np.array(list(zip(route.x, route.y)))
            return route

    def driveWay(o, d):
        KEY = '07ac12a00f830764ebfdee2fd0bc96fd'
        origin, destination = geocodeG(o)['geocodes'][0]['location'], geocodeG(d)['geocodes'][0]['location']
        if origin == None or destination == None:
            print("No stepWay")
            return None, None, None
        route = Route()
        route.o, route.d = o, d
        OUTPUT = 'json'
        url = 'https://restapi.amap.com/v3/direction/driving?parameters'
        params = {'origin': origin, 'destination': destination, 'key': KEY, 'output': OUTPUT}
        output = json.loads(requests.get(url, params).content)
        if output['status'] == '0' or output['count'] == 0:
            print("No Step Way")
            return None, None, None
        else:
            data = output['route']['paths'][0]['steps']
            route.type = "drive"
            route.dis = output['route']['paths'][0]['distance']
            route.time = output['route']['paths'][0]['duration']
            for li in data:
                route.note.append(li['instruction'])
                temp = li['polyline'].split(';')
                for k in temp:
                    k = k.split(',')
                    route.x.append(float(k[1]))
                    route.y.append(float(k[0]))
            route.route = np.array(list(zip(route.x, route.y)))
            return route

    def rideWay(o, d):
        KEY = '07ac12a00f830764ebfdee2fd0bc96fd'
        origin, destination = geocodeG(o)['geocodes'][0]['location'], geocodeG(d)['geocodes'][0]['location']
        if origin == None or destination == None:
            print("No stepWay")
            return None, None, None
        route = Route()
        route.o, route.d = o, d
        OUTPUT = 'json'
        url='https://restapi.amap.com/v3/direction/driving?parameters'
        params = {'origin': origin, 'destination': destination, 'key': KEY, 'output': OUTPUT, 'strategy': "9"}
        output = json.loads(requests.get(url, params).content)
        if ('status' in output.keys() and output['status'] == '0') or 'status' not in output.keys():
            print("No ride Way")
            return None, None, None
        else:
            data = output['route']['paths'][0]['steps']
            route.type = "drive"
            route.dis = output['route']['paths'][0]['distance']
            route.time = output['route']['paths'][0]['duration']
            for li in data:
                route.note.append(li['instruction'])
                temp = li['polyline'].split(';')
                for k in temp:
                    k = k.split(',')
                    route.x.append(float(k[1]))
                    route.y.append(float(k[0]))
            route.route = np.array(list(zip(route.x, route.y)))
            return route
    if approach==0:
        return rideWay(o,d)
    elif approach==1:
        return stepWay(o,d)
    else:
        return driveWay(o,d)
def loadCity():
    with open(path, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
    for data in json_data:
        print(data['area'], data['city'], data['province'], data['lat'], data['lng'])
def InitMap():
    # folium.CircleMarker(location=[30.696730, 104.033516],
    #                     radius=20, popup='成都', color='red', fill=True,
    #                     fill_color='red').add_to(m)
    m= folium.Map(location=[30.696730, 104.033516], zoom_start=12,
    tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    attr='default')
    data = io.BytesIO()
    m.save(data, close_file=False)
    return data,m
class QTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(QTabWidget, self).__init__(parent)
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下
            print("单击鼠标左键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.RightButton:  # 右键按下
            print("单击鼠标右键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton:  # 中键按下
            print("单击鼠标中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # 左右键同时按
            print("单击鼠标左右键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:  # 左中键同时按下
            print("单击鼠标左中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:  # 右中键同时按下
            print("单击鼠标右中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton \
                | QtCore.Qt.RightButton:  # 左中右键同时按下
            print("单击鼠标左中右键")  # 响应测试语句
    def wheelEvent(self, event):
        angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleX = angle.x()  # 水平滚过的距离(此处用不上)
        angleY = angle.y()  # 竖直滚过的距离
        if angleY > 0:
            print("鼠标滚轮上滚")  # 响应测试语句
        else:  # 滚轮下滚
            print("鼠标滚轮下滚")  # 响应测试语句
    def mouseDoubieCiickEvent(self, event):
        print("鼠标双击事件: 自己定义")
    def mouseReleaseEvent(self, event):
        print("鼠标释放")  # 响应测试语句
    def mouseMoveEvent(self, event):
        print("鼠标移动")  # 响应测试语句
class WebEngineView(QWebEngineView):
    def __init__(self,mainwindow,parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.create_tab(new_webview)
        return new_webview
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("路书")
        MainWindow.setWindowTitle('路书')
        MainWindow.resize(1112, 812)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(980, 340, 115, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(995, 40, 20, 20))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(850, 340, 115, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(830, 300, 54, 12))
        self.label.setText("")
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(945, 145, 141, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(850, 150, 90, 20))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(850, 430, 120, 40))
        self.save=QtWidgets.QLineEdit(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(990, 430, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(850, 480, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(850, 240, 110, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(850, 180, 231, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(900, 105, 200, 30))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(900, 65, 200, 30))
        self.lineEdit_5.setObjectName("lineEdit_5")
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(10)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(850, 75, 40, 20))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(850, 105, 40, 20))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(950, 290, 141, 31))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(990, 240, 60, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(850, 530, 241, 181))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(850, 720, 240, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(850, 290, 81, 30))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(850, 380, 240, 40))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(870, 0, 210, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setItalic(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1112, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.tabWidget.setGeometry(QtCore.QRect(0,0,840,760))
        MainWindow.setCentralWidget(self.centralwidget)
        self.webview=WebEngineView(self)

        navigation_bar = QToolBar('Navigation')# 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))# 添加导航栏到窗口中
        self.addToolBar(navigation_bar)
        back_button = QAction(QIcon(), 'Back', self)
        next_button = QAction(QIcon(), 'Forward', self)
        stop_button = QAction(QIcon(), 'stop', self)
        reload_button = QAction(QIcon(), 'reload', self)
        # 绑定事件
        back_button.triggered.connect(self.webview.back)
        next_button.triggered.connect(self.webview.forward)
        stop_button.triggered.connect(self.webview.stop)
        reload_button.triggered.connect(self.webview.reload)
        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        # 添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)
        # 让浏览器相应url地址的变化
        self.webview.urlChanged.connect(self.renew_urlbar)
        self.data,self.m= InitMap()
        self.webview.setHtml(self.data.getvalue().decode())
        self.create_tab(self.webview)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_1.setText(_translate("MainWindow", "^_^"))
        self.pushButton.setText(_translate("MainWindow", "启发式搜索"))
        self.pushButton_2.setText(_translate("MainWindow", "最短路搜索"))
        self.comboBox.setItemText(0, _translate("MainWindow", "骑行"))
        self.comboBox.setItemText(1, _translate("MainWindow", "行走"))
        self.comboBox.setItemText(2, _translate("MainWindow", "驾车"))
        self.label_2.setText(_translate("MainWindow", "出行方式"))
        self.pushButton_3.setText(_translate("MainWindow", "保存命名"))
        self.pushButton_4.setText(_translate("MainWindow", "从文件导入路线"))
        self.pushButton_5.setText(_translate("MainWindow", "添加中继点"))
        self.label_5.setText(_translate("MainWindow", "起点"))
        self.label_6.setText(_translate("MainWindow", "终点"))
        self.pushButton_6.setText(_translate("MainWindow", "撤回"))
        self.pushButton_7.setText(_translate("MainWindow", "保存备忘录"))
        self.label_7.setText(_translate("MainWindow", "全程距离"))
        self.pushButton_8.setText(_translate("MainWindow", "清空页面"))
        self.label_8.setText(_translate("MainWindow", " Code By CAMlive"))

    def create_tab(self,webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新标签页")
        self.tabWidget.setCurrentWidget(self.tab)
        self.Layout = QHBoxLayout(self.tab)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.addWidget(webview)
    def close_tab(self,index):
        if self.tabWidget.count()>1:
            self.tabWidget.removeTab(index)
        else:
            self.close()   # 当只有1个tab时，关闭主窗# 显示地址
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.webview.setUrl(q)# 响应输入的地址
    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
class MapData:
    def __init__(self):
        self.route=[]
        self.note=""
        self.dis=0
        self.time=0
        self.s=""
        self.d=""
class Map(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Map,self).__init__()
        self.mapData=MapData()
        self.setupUi(self)
        self.connecter()
        self.show()
    def connecter(self):
        self.pushButton.clicked.connect(self.getSD)
        self.pushButton_1.clicked.connect(self.playGame)
        self.pushButton_2.clicked.connect(self.getSD)
        self.pushButton_8.clicked.connect(self.reSet)
        self.pushButton_5.clicked.connect(self.addMid)
        self.pushButton_6.clicked.connect(self.BackMid)
        self.pushButton_3.clicked.connect(self.SaveWay)
        self.pushButton_4.clicked.connect(self.LoadWay)
        self.pushButton_7.clicked.connect(self.SaveNote)

        self.m.add_child(folium.LatLngPopup())
        self.m.add_child(folium.ClickForMarker(popup='Waypoint'))
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.webview.setHtml(self.data.getvalue().decode())
    def getSD(self):
        self.mapData.s=self.lineEdit_5.text()
        self.mapData.d=self.lineEdit_4.text()
        self.approach =int(self.comboBox.currentIndex())
        self.drawLine(self.mapData.route)
    def addMid(self):
        sender = self.sender()
        if sender == self.pushButton_5:
            text, ok = QInputDialog.getText(self, '添加中继点', '请输入中继点位置：')
            if ok:
                target=geocodeG(text)
                if target==None:
                    print("地址输入错误")
                else:
                    text=target['geocodes'][0]['formatted_address']
                    self.mapData.route.append(text)
                    self.textBrowser.append(text)
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
    def BackMid(self):
        if len(self.mapData.route)<=0:
            print("Error")
        else:
            self.mapData.route.pop()
            self.textBrowser.clear()
            for i,str in enumerate(self.mapData.route):
                self.textBrowser.append(str)
                self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
    def LoadWay(self):
        self.openPath, _ = QFileDialog.getOpenFileName()
        with open(self.openPath, 'rb') as file:
            map=pickle.loads(file.read())
        self.mapData=map
        self.drawLine(self.mapData.route)
        self.lineEdit_4.setText(self.mapData.d)
        self.lineEdit_5.setText(self.mapData.s)
    def SaveWay(self):
        savePath="Path.pkl"
        if self.save.text()!="":
            savePath=self.save.text()+".pkl"
        out_put = open(savePath, 'wb')
        map = pickle.dumps(self.mapData)
        out_put.write(map)
        out_put.close()
    def SaveNote(self):
        self.mapData.note=self.textEdit.toPlainText()
    def reSet(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textEdit.clear()
        self.save.clear()
        self.route=[]
        self.mapData = MapData()
        self.data,self.m=InitMap()
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.webview.setHtml(self.data.getvalue().decode())
    def playGame(self):
        print("112")
        self.webview=WebEngineView(self)
        self.webview.load(QUrl("http://www.baidu.com"))
        self.create_tab(self.webview)
    def plan(self,route):
        newRoute=[]
        newRoute.append(self.mapData.s)
        newRoute.extend(route)
        newRoute.append(self.mapData.d)
        tempR,tempN=[],[]
        tempD,tempT=0,0
        for i in range(len(newRoute)-1):
            tempRoute=Way(self.approach,newRoute[i],newRoute[i+1])
            print(tempRoute.dis,type(tempRoute.dis))
            tempD+=float(tempRoute.dis)
            tempT+=float(tempRoute.time)
            tempN.extend(tempRoute.note)
            tempR.extend(tempRoute.route)
        for note in tempN:
            self.textEdit.append(note)
        self.mapData.note=tempN
        self.mapData.dis=str(float(tempD/1000))
        self.mapData.time=str(float(tempT/60))
        self.textEdit.append("总时间"+self.mapData.time+"分钟")
        self.textBrowser_2.append(self.mapData.dis+"km")
        return tempR
    def drawLine(self,route):
        route=self.plan(route)
        folium.PolyLine(route,color='#3388ff').add_to(self.m)
        o=geocodeG(self.mapData.s)['geocodes'][0]['location']
        o=o.split(',')
        folium.Marker([float(o[1]),float(o[0])], color='red').add_to(self.m)
        d = geocodeG(self.mapData.d)['geocodes'][0]['location']
        d = d.split(',')
        folium.Marker([float(d[1]),float(d[0])], color='red').add_to(self.m)
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.webview.setHtml(self.data.getvalue().decode())
    def drawPoint(self,o,d):
        origin, destination = geocodeG(o)['geocodes'][0]['location'], geocodeG(d)['geocodes'][0]['location']
        folium.CircleMarker(location=origin,
        radius=10, popup='popup',color='red', fill=True,
                            fill_color='red').add_to(self.m)
        folium.CircleMarker(location=destination,
                            radius=10, popup='popup', color='red', fill=True,
                            fill_color='red').add_to(self.m)
        self.data=io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.webview.setHtml(self.data.getvalue().decode())
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win=Map()
    win.show()
    sys.exit(app.exec_())