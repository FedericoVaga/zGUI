# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zgui.ui'
#
# Created: Thu Mar 14 14:18:43 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_zGui(object):
    def setupUi(self, zGui):
        zGui.setObjectName(_fromUtf8("zGui"))
        zGui.resize(1024, 768)
        zGui.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        self.centralwidget = QtGui.QWidget(zGui)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.cmbCset = QtGui.QComboBox(self.centralwidget)
        self.cmbCset.setGeometry(QtCore.QRect(90, 40, 121, 25))
        self.cmbCset.setObjectName(_fromUtf8("cmbCset"))
        self.lblCset = QtGui.QLabel(self.centralwidget)
        self.lblCset.setGeometry(QtCore.QRect(20, 40, 60, 25))
        self.lblCset.setObjectName(_fromUtf8("lblCset"))
        self.lblChan = QtGui.QLabel(self.centralwidget)
        self.lblChan.setGeometry(QtCore.QRect(20, 130, 60, 25))
        self.lblChan.setObjectName(_fromUtf8("lblChan"))
        self.cmbChan = QtGui.QComboBox(self.centralwidget)
        self.cmbChan.setGeometry(QtCore.QRect(90, 130, 121, 25))
        self.cmbChan.setObjectName(_fromUtf8("cmbChan"))
        self.zTab = QtGui.QTabWidget(self.centralwidget)
        self.zTab.setGeometry(QtCore.QRect(20, 400, 991, 301))
        self.zTab.setObjectName(_fromUtf8("zTab"))
        self.tabDev = QtGui.QWidget()
        self.tabDev.setObjectName(_fromUtf8("tabDev"))
        self.zTab.addTab(self.tabDev, _fromUtf8(""))
        self.tabCset = QtGui.QWidget()
        self.tabCset.setObjectName(_fromUtf8("tabCset"))
        self.zTab.addTab(self.tabCset, _fromUtf8(""))
        self.tabBuf = QtGui.QWidget()
        self.tabBuf.setObjectName(_fromUtf8("tabBuf"))
        self.zTab.addTab(self.tabBuf, _fromUtf8(""))
        self.tabTrig = QtGui.QWidget()
        self.tabTrig.setObjectName(_fromUtf8("tabTrig"))
        self.zTab.addTab(self.tabTrig, _fromUtf8(""))
        self.tabChan = QtGui.QWidget()
        self.tabChan.setObjectName(_fromUtf8("tabChan"))
        self.zTab.addTab(self.tabChan, _fromUtf8(""))
        self.cmbDev = QtGui.QComboBox(self.centralwidget)
        self.cmbDev.setGeometry(QtCore.QRect(90, 10, 121, 25))
        self.cmbDev.setObjectName(_fromUtf8("cmbDev"))
        self.lblDev = QtGui.QLabel(self.centralwidget)
        self.lblDev.setGeometry(QtCore.QRect(20, 10, 60, 25))
        self.lblDev.setObjectName(_fromUtf8("lblDev"))
        self.lblBuf = QtGui.QLabel(self.centralwidget)
        self.lblBuf.setGeometry(QtCore.QRect(20, 70, 60, 25))
        self.lblBuf.setObjectName(_fromUtf8("lblBuf"))
        self.cmbBuf = QtGui.QComboBox(self.centralwidget)
        self.cmbBuf.setGeometry(QtCore.QRect(90, 70, 121, 25))
        self.cmbBuf.setObjectName(_fromUtf8("cmbBuf"))
        self.lblTrig = QtGui.QLabel(self.centralwidget)
        self.lblTrig.setGeometry(QtCore.QRect(20, 100, 60, 25))
        self.lblTrig.setObjectName(_fromUtf8("lblTrig"))
        self.cmbTrig = QtGui.QComboBox(self.centralwidget)
        self.cmbTrig.setGeometry(QtCore.QRect(90, 100, 121, 25))
        self.cmbTrig.setObjectName(_fromUtf8("cmbTrig"))
        self.btnAcq = QtGui.QPushButton(self.centralwidget)
        self.btnAcq.setGeometry(QtCore.QRect(90, 355, 120, 25))
        self.btnAcq.setObjectName(_fromUtf8("btnAcq"))
        self.ckbNShow = QtGui.QCheckBox(self.centralwidget)
        self.ckbNShow.setGeometry(QtCore.QRect(20, 160, 190, 25))
        self.ckbNShow.setObjectName(_fromUtf8("ckbNShow"))
        self.ckbPoint = QtGui.QCheckBox(self.centralwidget)
        self.ckbPoint.setGeometry(QtCore.QRect(20, 180, 190, 25))
        self.ckbPoint.setObjectName(_fromUtf8("ckbPoint"))
        self.ckbContinuous = QtGui.QCheckBox(self.centralwidget)
        self.ckbContinuous.setGeometry(QtCore.QRect(20, 200, 190, 25))
        self.ckbContinuous.setObjectName(_fromUtf8("ckbContinuous"))
        zGui.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(zGui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        zGui.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(zGui)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        zGui.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(zGui)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        zGui.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionExit = QtGui.QAction(zGui)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(zGui)
        self.zTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(zGui)

    def retranslateUi(self, zGui):
        zGui.setWindowTitle(_translate("zGui", "MainWindow", None))
        self.lblCset.setText(_translate("zGui", "Csets", None))
        self.lblChan.setText(_translate("zGui", "Channels", None))
        self.zTab.setTabText(self.zTab.indexOf(self.tabDev), _translate("zGui", "Device", None))
        self.zTab.setTabText(self.zTab.indexOf(self.tabCset), _translate("zGui", "Channel Sets", None))
        self.zTab.setTabText(self.zTab.indexOf(self.tabBuf), _translate("zGui", "Buffer", None))
        self.zTab.setTabText(self.zTab.indexOf(self.tabTrig), _translate("zGui", "Trigger", None))
        self.zTab.setTabText(self.zTab.indexOf(self.tabChan), _translate("zGui", "Channels", None))
        self.lblDev.setText(_translate("zGui", "Devices", None))
        self.lblBuf.setText(_translate("zGui", "Buffer", None))
        self.lblTrig.setText(_translate("zGui", "Trigger", None))
        self.btnAcq.setText(_translate("zGui", "Acquire", None))
        self.ckbNShow.setText(_translate("zGui", "Show all channel", None))
        self.ckbPoint.setText(_translate("zGui", "Show points", None))
        self.ckbContinuous.setText(_translate("zGui", "Continuous acquisition", None))
        self.menuFile.setTitle(_translate("zGui", "File", None))
        self.toolBar.setWindowTitle(_translate("zGui", "toolBar", None))
        self.actionExit.setText(_translate("zGui", "Exit", None))
        self.actionExit.setShortcut(_translate("zGui", "Ctrl+Q", None))

