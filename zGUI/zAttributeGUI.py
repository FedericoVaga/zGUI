"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
from PyQt4 import QtCore, QtGui

class zAttributeGUI(object):
    """It creates and it handles the GUI for a ZIO attribute"""
    def __init__(self, zGUI, parent, attr, x, y):
        """Create the GUI to handle an attribute. It creates (ASCII art):
        Label [field] [Get][Set]"""
        self.zGUI = zGUI
        self.attr = attr
        # Create the label
        self.lbl = QtGui.QLabel(parent)
        self.lbl.setGeometry(QtCore.QRect(x, y, 100, 25))
        self.lbl.setText(attr.name)
        self.lbl.setObjectName(attr.name)
        self.lbl.show()
        # Create the edit field
        self.edt = QtGui.QLineEdit(parent)
        self.edt.setGeometry(QtCore.QRect(x + 100 , y, 150, 25))
        self.edt.setObjectName("edit")
        self.edt.setText(self.attr.getValue())
        self.edt.show()
        # Create the Set button to set the value to the attribute
        self.btnSet = QtGui.QPushButton("Set",parent)
        self.btnSet.setGeometry(QtCore.QRect(x + 250 , y, 40, 25))
        self.btnSet.setObjectName("write")
        self.btnSet.setEnabled(attr.isWritable())
        if self.btnSet.isEnabled():
            self.btnSet.clicked.connect(self.__btnSetClick)
        self.btnSet.show()
        # Create the get button to get the last value of the attribute
        self.btnGet = QtGui.QPushButton("Get", parent)
        self.btnGet.setGeometry(QtCore.QRect(x + 290 , y, 40, 25))
        self.btnGet.setObjectName("read")
        self.btnGet.setEnabled(attr.isReadable())
        if self.btnGet.isEnabled():
            self.btnGet.clicked.connect(self.__btnGetClick)
        self.btnGet.show()
        pass

    def __del__(self):
        """Destroy the GUI"""
        self.btnGet.setParent(None)
        self.btnSet.setParent(None)
        self.lbl.setParent(None)
        self.edt.setParent(None)
        pass

    def refreshValue(self):
        self.edt.setText(self.attr.getValue())
        pass

    # PRIVATE FUNCTIONS

    def __btnSetClick(self):
        """It gets a value from the edit field and it sets to the attribute.
        Then it refresh the GUI with the current value of the attribute. It
        should be the setted one, but if the driver refuse the value it can be
        a different value"""
        self.attr.setValue(self.edt.text())
        self.zGUI.refreshAttributes()
        pass

    def __btnGetClick(self):
        """It update the edit field with the current value of the attirbute"""
        self.refreshValue()
        pass
