"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
from PyQt4 import QtCore, QtGui

class attributeGUI(object):
    def __init__(self, zGUI, parent, attr, x, y):
        self.zGUI = zGUI
        self.attr = attr

        self.lbl = QtGui.QLabel(parent)
        self.lbl.setGeometry(QtCore.QRect(x, y, 100, 25))
        self.lbl.setText(attr.name)
        self.lbl.setObjectName(attr.name)
        self.lbl.show()

        self.edt = QtGui.QLineEdit(parent)
        self.edt.setGeometry(QtCore.QRect(x + 100 , y, 150, 25))
        self.edt.setObjectName("edit")
        self.edt.setText(self.attr.getValue())
        self.edt.show()

        self.btnSet = QtGui.QPushButton("Set",parent)
        self.btnSet.setGeometry(QtCore.QRect(x + 250 , y, 40, 25))
        self.btnSet.setObjectName("write")
        self.btnSet.setEnabled(attr.writable)
        if self.btnSet.isEnabled():
            self.btnSet.clicked.connect(self.btnSetClick)
        self.btnSet.show()

        self.btnGet = QtGui.QPushButton("Get", parent)
        self.btnGet.setGeometry(QtCore.QRect(x + 290 , y, 40, 25))
        self.btnGet.setObjectName("read")
        self.btnGet.setEnabled(attr.readable)
        if self.btnGet.isEnabled():
            self.btnGet.clicked.connect(self.btnGetClick)
        self.btnGet.show()
        pass

    def __del__(self):
        self.btnGet.setParent(None)
        self.btnSet.setParent(None)
        self.lbl.setParent(None)
        self.edt.setParent(None)
        pass

    def refreshValue(self):
        self.edt.setText(self.attr.getValue())
        pass

    def btnSetClick(self):
        self.attr.setValue(self.edt.text())
        self.zGUI.refreshAttributes()
        pass

    def btnGetClick(self):
        self.refreshValue()
        pass
