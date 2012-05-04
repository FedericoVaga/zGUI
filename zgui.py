# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zgui.ui'
#
# Created: Mon Feb 27 13:08:29 2012
#      by: pyside-uic 0.2.13 running on PySide 1.0.8
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from config import *
import util
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *

class attributeGUI(QtGui.QWidget):
    def __init__(self, zGUI, parent, attr, x, y):
        self.zGUI = zGUI
        self.attr = attr
        self.lbl = QtGui.QLabel(parent)
        self.lbl.setGeometry(QtCore.QRect(x, y, 100, 25))
        self.lbl.setText(attr.name)
        self.lbl.setObjectName(attr.name)
        
        self.edt = QtGui.QLineEdit(parent)
        self.edt.setGeometry(QtCore.QRect(x + 100 , y, 150, 25))
        self.edt.setObjectName("edit")
        self.edt.setText(self.attr.read())
        
        self.btnSet = QtGui.QPushButton("Set",parent)
        self.btnSet.setGeometry(QtCore.QRect(x + 250 , y, 40, 25))
        self.btnSet.setObjectName("write")
        self.btnSet.setEnabled(attr.writable)
        if self.attr.writable:
            self.btnSet.clicked.connect(self.__btnSetClick)
        
        self.btnGet = QtGui.QPushButton("Get", parent)
        self.btnGet.setGeometry(QtCore.QRect(x + 290 , y, 40, 25))
        self.btnGet.setObjectName("read")
        self.btnGet.setEnabled(attr.readable)
        if self.attr.readable:
            self.btnGet.clicked.connect(self.__btnGetClick)
        
    def __del__(self):
        self.btnGet.setParent(None)
        self.btnSet.setParent(None)
        self.lbl.setParent(None)
        self.edt.setParent(None)
        
    def refreshValue(self):
        self.edt.setText(self.attr.read())
        
    def __btnSetClick(self):
        print("ciao")
        self.attr.write(self.edt.text())
        self.zGUI.refreshAttributes()
        
    def __btnGetClick(self):
        print("ciao")
        self.refreshValue()

class Ui_zGui(object):
    def setupUi(self, zGui):
        zGui.setObjectName("zGui")
        zGui.resize(1003, 799)
        zGui.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        self.centralwidget = QtGui.QWidget(zGui)
        self.centralwidget.setObjectName("centralwidget")
        
        self.zdevAttr = []
        self.csetAttr = []
        self.trigAttr = []
        self.zbufAttr = []
        self.chanAttr = []
        
        # create tab frame
        self.zTab = QtGui.QTabWidget(self.centralwidget)
        self.zTab.setGeometry(QtCore.QRect(20, 400, 971, 301))
        self.zTab.setObjectName("zTab")
        
        # Graph
        self.graph = QtGui.QGraphicsView(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(220, 10, 770, 380))
        self.graph.setObjectName("Graph")
        # pick the background color from parent (the main window)
        self.graph.setBackgroundRole(QPalette.NoRole)

        # Device Tab
        self.zdev = QtGui.QWidget()
        self.zdev.setObjectName("zdev")
        self.zTab.addTab(self.zdev, "")
        
        # Channel Set tab
        self.cset = QtGui.QWidget()
        self.cset.setObjectName("cset")
        self.zTab.addTab(self.cset, "")
        
        # Buffer tab
        self.zbuf = QtGui.QWidget()
        self.zbuf.setObjectName("zbuf")
        self.zTab.addTab(self.zbuf, "")
        
        # Trigger tab
        self.trig = QtGui.QWidget()
        self.trig.setObjectName("trig")
        self.zTab.addTab(self.trig, "")
        
        # Channel tab
        self.chan = QtGui.QWidget()
        self.chan.setObjectName("chan")
        self.zTab.addTab(self.chan, "")
        
        # Device Combobox
        self.lblDev = QtGui.QLabel(self.centralwidget)
        self.lblDev.setGeometry(QtCore.QRect(20, 10, 60, 25))
        self.lblDev.setObjectName("lblDev")
        self.cmbDev = QtGui.QComboBox(self.centralwidget)
        self.cmbDev.setGeometry(QtCore.QRect(90, 10, 120, 25))
        self.cmbDev.setObjectName("cmbDev")
        self.cmbDev.currentIndexChanged.connect(self.changeDevice)
        
        # Channel Set Combobox
        self.lblCset = QtGui.QLabel(self.centralwidget)
        self.lblCset.setGeometry(QtCore.QRect(20, 50, 60, 25))
        self.lblCset.setObjectName("lblCset")
        self.cmbCset = QtGui.QComboBox(self.centralwidget)
        self.cmbCset.setGeometry(QtCore.QRect(90, 50, 120, 25))
        self.cmbCset.setObjectName("cmbCset")
        self.cmbCset.currentIndexChanged.connect(self.changeCset)
        
         # Buffer Combobox
        self.lblBuf = QtGui.QLabel(self.centralwidget)
        self.lblBuf.setGeometry(QtCore.QRect(20, 90, 60, 25))
        self.lblBuf.setObjectName("lblBuf")
        self.cmbBuf = QtGui.QComboBox(self.centralwidget)
        self.cmbBuf.setGeometry(QtCore.QRect(90, 90, 120, 25))
        self.cmbBuf.setObjectName("cmbBuf")
        self.cmbBuf.currentIndexChanged.connect(self.changeBuffer)
        
        #Trigger Combobox
        self.lblTrig = QtGui.QLabel(self.centralwidget)
        self.lblTrig.setGeometry(QtCore.QRect(20, 130, 60, 25))
        self.lblTrig.setObjectName("lblTrig")
        self.cmbTrig = QtGui.QComboBox(self.centralwidget)
        self.cmbTrig.setGeometry(QtCore.QRect(90, 130, 120, 25))
        self.cmbTrig.setObjectName("cmbTrig")
        self.cmbTrig.currentIndexChanged.connect(self.changeTrigger)
        
        # Channel combobox
        self.lblChan = QtGui.QLabel(self.centralwidget)
        self.lblChan.setGeometry(QtCore.QRect(20, 170, 60, 25))
        self.lblChan.setObjectName("lblChan")
        self.cmbChan = QtGui.QComboBox(self.centralwidget)
        self.cmbChan.setGeometry(QtCore.QRect(90, 170, 120, 25))
        self.cmbChan.setObjectName("cmbChan")
        self.cmbChan.currentIndexChanged.connect(self.changeChan)
        
        # Acquire Button
        self.btnAcq = QtGui.QPushButton("Acquire", self.centralwidget)
        self.btnAcq.setGeometry(QtCore.QRect( 90 , 210, 120, 25))
        self.btnAcq.clicked.connect(self.acquireClick)
        
        zGui.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(zGui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1003, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        zGui.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(zGui)
        self.statusbar.setObjectName("statusbar")
        zGui.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(zGui)
        self.toolBar.setObjectName("toolBar")
        zGui.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtGui.QAction(zGui)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(zGui)
        self.zTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(zGui)

    def refreshDevice(self):
        self.cmbDev.clear()
        names = []
        for d in devices:
            names.append(d.name)
        self.cmbDev.addItems(names)

    def acquireClick(self):
        
        scene = QtGui.QGraphicsScene()
        data = devices[self.d_i].cset[self.cs_i].chan[self.ch_i].datacdev.readData(True, True)
        print(data)
        p = Plot(Curve(range(len(data)),\
                data,\
                Pen(Red, 1),\
                Symbol(Circle, Black),\
                "data"))
        p.setGeometry(QtCore.QRect(0, 0, 750, 370))
        scene.addPixmap(QPixmap.grabWidget(p))
        self.graph.setScene(scene);
        self.graph.show();
        
    #
    # Functions for combobox change
    #
    def changeDevice(self, i):
        self.d_i = i
        # add device cset to correspondent combobox
        self.cmbCset.clear()
        self.cmbCset.addItems(devices[i].getCsetsName())
        
        x = 10
        y = 10
        del self.zdevAttr[:]
        attrs = devices[self.d_i].attribute
        for attr in attrs:
            self.zdevAttr.append(attributeGUI(self, self.zdev, attrs[attr], x, y))
            y += 30

    def changeCset(self, i):
        self.cs_i = i
        self.cmbChan.clear()
        self.cmbChan.addItems(devices[self.d_i].cset[i].getChansName())
        
        x = 10
        y = 10
        del self.csetAttr[:]
        attrs = devices[self.d_i].cset[self.cs_i].attribute
        for attr in attrs:
            self.csetAttr.append(attributeGUI(self, self.cset, attrs[attr], x, y))
            y += 30
            
        # update buffer
        self.cmbBuf.clear()
        self.b_i = None
        for b in buffers:
            self.cmbBuf.addItem(b)
        self.b_i = 0
        bufName = devices[self.d_i].cset[i].attribute['current_buffer'].read()
        self.cmbBuf.setCurrentIndex(self.cmbBuf.findText(bufName))
        
        # update trigger
        self.cmbTrig.clear()
        self.t_i = None
        for t in triggers:
            self.cmbTrig.addItem(t)
        self.t_i = 0
        trigName = devices[self.d_i].cset[i].getCurrentTrigger()
        self.cmbTrig.setCurrentIndex(self.cmbTrig.findText(trigName))

    def changeBuffer(self, i):
        if self.b_i == None:
            return
        self.b_i = i
        text = self.cmbBuf.itemText(i)
        print("Change Buffer to " + text)
        devices[self.d_i].cset[self.cs_i].setCurrentBuffer(text)
        x = 10
        y = 10
        del self.zbufAttr[:]
        attrs = devices[self.d_i].cset[self.cs_i].chan[self.ch_i].buffer.attribute
        for attr in attrs:
            self.zbufAttr.append(attributeGUI(self, self.zbuf, attrs[attr], x, y))
            y += 30

    def changeTrigger(self, i):
        if self.t_i == None:
            return
        self.t_i = i
        text = self.cmbTrig.itemText(i)
        print("Change Trigger to " + text)
        devices[self.d_i].cset[self.cs_i].setCurrentTrigger(text)
        
        x = 10
        y = 10
        del self.trigAttr[:]
        attrs = devices[self.d_i].cset[self.cs_i].trigger.attribute
        for attr in attrs:
            self.trigAttr.append(attributeGUI(self, self.trig, attrs[attr], x, y))
            y += 30

    def changeChan(self, i):
        self.ch_i = i
        
        x = 10
        y = 10
        del self.chanAttr[:]
        attrs = devices[self.d_i].cset[self.cs_i].chan[i].attribute
        for attr in attrs:
            self.chanAttr.append(attributeGUI(self, self.chan, attrs[attr], x, y))
            y += 30

    def refreshAttributes(self):
        for attrGUI in self.chanAttr:
            attrGUI.refreshValue()
        for attrGUI in self.csetAttr:
            attrGUI.refreshValue()
        for attrGUI in self.zdevAttr:
            attrGUI.refreshValue()
        for attrGUI in self.trigAttr:
            attrGUI.refreshValue()
        for attrGUI in self.zbufAttr:
            attrGUI.refreshValue()
    #
    # GUI function
    #
    def retranslateUi(self, zGui):
        zGui.setWindowTitle(QtGui.QApplication.translate("zGui", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCset.setText(QtGui.QApplication.translate("zGui", "Csets", None, QtGui.QApplication.UnicodeUTF8))
        self.lblChan.setText(QtGui.QApplication.translate("zGui", "Channels", None, QtGui.QApplication.UnicodeUTF8))
        self.zTab.setTabText(self.zTab.indexOf(self.zdev), QtGui.QApplication.translate("zGui", "Device", None, QtGui.QApplication.UnicodeUTF8))
        self.zTab.setTabText(self.zTab.indexOf(self.cset), QtGui.QApplication.translate("zGui", "Channel Sets", None, QtGui.QApplication.UnicodeUTF8))
        self.zTab.setTabText(self.zTab.indexOf(self.zbuf), QtGui.QApplication.translate("zGui", "Buffer", None, QtGui.QApplication.UnicodeUTF8))
        self.zTab.setTabText(self.zTab.indexOf(self.trig), QtGui.QApplication.translate("zGui", "Trigger", None, QtGui.QApplication.UnicodeUTF8))
        self.zTab.setTabText(self.zTab.indexOf(self.chan), QtGui.QApplication.translate("zGui", "Channels", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDev.setText(QtGui.QApplication.translate("zGui", "Devices", None, QtGui.QApplication.UnicodeUTF8))
        self.lblBuf.setText(QtGui.QApplication.translate("zGui", "Buffer", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTrig.setText(QtGui.QApplication.translate("zGui", "Trigger", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("zGui", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("zGui", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("zGui", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("zGui", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))

def refreshDevices():
    util.getAvailableDevices()

if __name__ == "__main__":
    import sys
    util.getAvailableBuffers()
    util.getAvailableTriggers()
    refreshDevices()
    
    app = QtGui.QApplication(sys.argv)
    zGui = QtGui.QMainWindow()
    ui = Ui_zGui()
    ui.setupUi(zGui)
    ui.refreshDevice()
    zGui.show()
   
    sys.exit(app.exec_())


