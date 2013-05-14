"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""
from PyQt4 import QtGui

class ZioAttributeGUI(object):
    """It creates and it handles the GUI for a ZIO attribute"""
    def __init__(self, zgui, parent, attr):
        """Create the GUI to handle an attribute. It creates (ASCII art):
        Label [field] [Get][Set]"""
        self.zgui = zgui
        self.attr = attr
        # Create the label
        self.lbl = QtGui.QLabel(parent)
        self.lbl.setText(attr.name)
        self.lbl.setObjectName(attr.name)
        self.lbl.show()
        # Create the edit field
        self.edt = QtGui.QLineEdit(parent)
        self.edt.setObjectName("edit")
        self.refresh_value()
        self.edt.show()
        # Create the Set button to set the value to the attribute
        self.btnSet = QtGui.QPushButton("Set",parent)
        self.btnSet.setObjectName("write")
        self.btnSet.setEnabled(attr.is_writable())
        if self.btnSet.isEnabled():
            self.btnSet.clicked.connect(self.__btn_set_click)
        self.btnSet.show()
        # Create the get button to get the last value of the attribute
        self.btnGet = QtGui.QPushButton("Get", parent)
        self.btnGet.setObjectName("read")
        self.btnGet.setEnabled(attr.is_readable())
        if self.btnGet.isEnabled():
            self.btnGet.clicked.connect(self.__btn_get_click)
        self.btnGet.show()
        pass

    def __del__(self):
        """Destroy the GUI"""
        self.btnGet.setParent(None)
        self.btnSet.setParent(None)
        self.lbl.setParent(None)
        self.edt.setParent(None)
        pass

    def refresh_value(self):
        if self.attr.is_readable():
                self.edt.setText(self.attr.get_value())
        pass

    # PRIVATE FUNCTIONS

    def __btn_set_click(self):
        """It gets a value from the edit field and it sets to the attribute.
        Then it refresh the GUI with the current value of the attribute. It
        should be the setted one, but if the driver refuse the value it can be
        a different value"""
        self.attr.set_value(self.edt.text())
        self.zgui.refresh_attributes()
        pass

    def __btn_get_click(self):
        """It update the edit field with the current value of the attirbute"""
        self.refresh_value()
        pass
