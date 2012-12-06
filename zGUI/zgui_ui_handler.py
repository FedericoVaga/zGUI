"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

from PyQt4 import QtCore, QtGui
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *

from PyZio import *
from PyZio.zUtil import *
from .attributegui import attributeGUI

import random

class ui_handler(object):
    def __init__(self, ui):
        self.ui = ui

        self.color_index = 0;
        self.color = [Black, Red, Yellow, Cyan, Magenta, Green, Blue]
        self.zdevAttr = []
        self.csetAttr = []
        self.trigAttr = []
        self.zbufAttr = []
        self.chanAttr = []
        self.d_i =  None
        self.cs_i = None
        self.ch_i = None
        self.b_i =  None
        self.t_i =  None

        # Configure Events
        self.updateAvailableObject(buffers, self.ui.cmbBuf)
        self.updateAvailableObject(triggers, self.ui.cmbTrig)

        self.ui.cmbDev.currentIndexChanged.connect(self.changeDevice)
        self.ui.cmbCset.currentIndexChanged.connect(self.changeCset)
        self.ui.cmbChan.currentIndexChanged.connect(self.changeChan)
        self.ui.cmbBuf.currentIndexChanged.connect(self.changeBuffer)
        self.ui.cmbTrig.currentIndexChanged.connect(self.changeTrigger)
        self.ui.btnAcq.clicked.connect(self.acquireClick)
        self.ui.actionExit.triggered.connect(exit)


        # Looks for devices
        self.refreshDevice()

    def refreshDevice(self):
        self.ui.cmbDev.clear()
        names = []
        for d in devices:
            names.append(d.name)
        self.ui.cmbDev.addItems(names)

    def updateAvailableObject(self, avList, comboBox):
        comboBox.clear()
        names = []
        for name in avList:
            names.append(name)
        comboBox.addItems(names)

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
        pass

    def __acquireChan(self, chan):
        """Acquire data from channel and draw its curve"""
        chan.interface.readBlock()
        data = chan.interface.getSamples()
        if data == None:
            return None # not plottable
        color = QColor(random.randint(0, 255), random.randint(0,255), random.randint(0,255))

        name = chan.name + " (" + str(chan.interface.ctrl.seq_num) + ")"
        if self.ui.ckbPoint.isChecked():
            c = Curve(range(len(data)), data, Pen(color, 2), Symbol(Circle, Black, 4), name)
        else:
            c = Curve(range(len(data)), data, Pen(color, 2), name)
        return c

    def acquireClick(self):
        """Event associated to the click on the acquire button. When
        invoked, it acquires on all requested channel"""

        if self.d_i == None or self.cs_i == None or self.ch_i == None:
            print("Select channel before acquire")
            return
        # Initialize the list of curves to draw
        curves = []

        # If the user wants to display all the channels, then add all
        # curves to the list ...
        if self.ui.ckbNShow.isChecked():
            for chan in devices[self.d_i].cset[self.cs_i].chan:
                curves.append(self.__acquireChan(chan))
        # ... otherwise add only the selected channel's curve
        else:
            chan = devices[self.d_i].cset[self.cs_i].chan[self.ch_i]
            curves.append(self.__acquireChan(chan))
        # Create a plot of curves
        p = Plot("Data")
        for c in curves:
            if c == None:
                print("Cannot plot None")
                continue
            p.plot(c)
        p.setGeometry(QtCore.QRect(0, 0, 755, 365))
        # Show in the GUI the plot
        scene = QtGui.QGraphicsScene()
        scene.addPixmap(QPixmap.grabWidget(p))
        self.ui.graph.setScene(scene)
        self.ui.graph.show()
        pass

    def __refreshAttributesGUI(self, tab, attrListGUI, attrsList):
        """Remove old attributes and update the GUI with new ones"""
        x = 10
        y = 10
        del attrListGUI[:]
        for attr in attrsList:
            attrListGUI.append(attributeGUI(self, tab, attrsList[attr], x, y))
            y += 30
        pass

    def changeDevice(self, i):
        """Change selected device"""
        self.d_i = i
        # add device cset to correspondent combobox
        self.ui.cmbCset.clear()
        for chan in devices[self.d_i].cset:
            self.ui.cmbCset.addItem(chan.name)
        self.__refreshAttributesGUI(self.ui.tabDev, self.zdevAttr, devices[self.d_i].attribute)
        pass

    def changeCset(self, i):
        """Change selected cset"""
        self.cs_i = i
        self.ui.cmbChan.clear()
        for chan in devices[self.d_i].cset[i].chan:
            self.ui.cmbChan.addItem(chan.name)
        self.__refreshAttributesGUI(self.ui.tabCset, self.csetAttr, devices[self.d_i].cset[self.cs_i].attribute)

        # update buffer
        bufName = devices[self.d_i].cset[i].attribute['current_buffer'].getValue()
        i = self.ui.cmbBuf.findText(bufName)
        self.ui.cmbBuf.setCurrentIndex(i)
        if self.b_i == None: # for initialization
            self.changeBuffer(i)

        # update trigger
        trigName = devices[self.d_i].cset[self.cs_i].getCurrentTrigger()
        i = self.ui.cmbTrig.findText(trigName)
        self.ui.cmbTrig.setCurrentIndex(i)
        if self.t_i == None: # for initialization
            self.changeTrigger(i)
        pass

    def changeBuffer(self, i):
        """Change selected buffer"""
        if self.d_i == None or self.cs_i == None:
            print("Select channel set before change buffer")
            self.ui.cmbBuf.setCurrentIndex(0)
            return
        self.b_i = i
        text = self.ui.cmbBuf.itemText(self.b_i)
        devices[self.d_i].cset[self.cs_i].setCurrentBuffer(text)
        print("Change Buffer to " + text)
        self.__refreshAttributesGUI(self.ui.tabBuf, self.zbufAttr, devices[self.d_i].cset[self.cs_i].chan[self.ch_i].buffer.attribute)
        pass

    def changeTrigger(self, i):
        """Change selected trigger"""
        if self.d_i == None or self.cs_i == None:
            print("Select channel set before change trigger")
            self.ui.cmbTrig.setCurrentIndex(0)
            return
        self.t_i = i
        text = self.ui.cmbTrig.itemText(i)
        devices[self.d_i].cset[self.cs_i].setCurrentTrigger(text)
        print("Change Trigger to " + text)
        self.__refreshAttributesGUI(self.ui.tabTrig, self.trigAttr, devices[self.d_i].cset[self.cs_i].trigger.attribute)
        pass

    def changeChan(self, i):
        """Change selected channel"""
        self.ch_i = i
        self.__refreshAttributesGUI(self.ui.tabChan, self.chanAttr, devices[self.d_i].cset[self.cs_i].chan[i].attribute)
        pass