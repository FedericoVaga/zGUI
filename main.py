#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A simple interface to ZIO

author: Federico Vaga
last edited: February 2012
"""

import sys
import os
from sysfs import *
from PyQt4 import QtGui, QtCore

class zMainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(zMainWindow, self).__init__()
        
        self.initUI()
    
    # Initialize user interface
    def initUI(self):
        
        
        exitAction = QtGui.QAction(QtGui.QIcon('images/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q') # short cut
        exitAction.setStatusTip('Exit application') # showed on status bar
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        devMenu = menubar.addMenu('&Devices')
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        
        lbl1 = QtGui.QLabel('Devices', self)
        lbl1.move(15, 10)
        cmbDevices = QtGui.QComboBox(self)
        cmbDevices.move(100, 10)
        cmbDevices.addItems(devices)
        
        cmbCsets = QtGui.QComboBox(self)
        
        btn = QtGui.QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        
        self.resize(512, 512)
        self.center()
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('images/zeta.png'))
    
        self.show()
        self.statusBar().showMessage('Ready')

    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
def main():

    # check if zio is loaded
    if not os.access(devices_path, os.F_OK):
        print "ZIO is not loaded, missing ZIO bus"
        exit()

    app = QtGui.QApplication(sys.argv)
    ex = zMainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()