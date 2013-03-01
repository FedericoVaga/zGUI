"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

from PyQt4 import QtCore, QtGui

from PyQt4.Qwt5.qplt import Circle, QPixmap
from PyQt4.Qwt5.qplt import Plot, Pen, Curve, QColor, Symbol
from PyQt4.Qwt5.qplt import Black, Red, Yellow, Cyan, Magenta, Green, Blue

from PyZio import ZioUtil
from PyZio.ZioDev import ZioDev
from PyZio.ZioConfig import buffers, triggers, devices, devices_path
from zGUI.ZioAttributeGUI import ZioAttributeGUI

import random

class ZioGuiHandler(object):
    def __init__(self, ui):
        """It initialize the GUI and connect GUI events"""
        self.ui = ui

        self.zdevlist = []
        self.color_index = 0;
        self.color = [Red, Green, Blue, Black, Yellow, Cyan, Magenta]
        self.zdev_attr = []
        self.cset_attr = []
        self.trig_attr = []
        self.buf_attr = []
        self.chan_attr = []
        self.d_i = None
        self.cs_i = None
        self.ch_i = None
        self.b_i = None
        self.t_i = None

        # Configure Events
        self.ui.cmbDev.currentIndexChanged.connect(self.change_device)
        self.ui.cmbCset.currentIndexChanged.connect(self.change_cset)
        self.ui.cmbChan.currentIndexChanged.connect(self.change_chan)
        self.ui.cmbBuf.currentIndexChanged.connect(self.change_buffer)
        self.ui.cmbTrig.currentIndexChanged.connect(self.change_trigger)
        self.ui.btnAcq.clicked.connect(self.acquire_click)
        self.ui.actionExit.triggered.connect(exit)

        self.refresh_device()# Looks for devices

    def refresh_device(self):
        """It checks for devices"""
        ZioUtil.update_devices()
        del self.zdevlist[:]
        for zdev in devices:
            self.zdevlist.append(ZioDev(devices_path, zdev))

        # Update the device combo box
        self.update_object_list(devices, self.ui.cmbDev)
        self.update_object_list(buffers, self.ui.cmbBuf)
        self.update_object_list(triggers, self.ui.cmbTrig)


    def update_object_list(self, available_list, combo_box):
        """It updates the object within a list and the corresponded combo box"""
        combo_box.clear()
        names = []
        for name in available_list:
            names.append(name)
        combo_box.addItems(names)


    def refresh_attributes(self):
        """It refresh all the attribute showed in the GUI"""
        for agui in self.chan_attr:
            agui.refresh_value()
        for agui in self.cset_attr:
            agui.refresh_value()
        for agui in self.zdev_attr:
            agui.refresh_value()
        for agui in self.trig_attr:
            agui.refresh_value()
        for agui in self.buf_attr:
            agui.refresh_value()

    def __acquire_chan(self, chan, i):
        """Acquire data from channel and draw its curve"""
        ctrl, data = chan.interface.read_block(True, True)
        if data == None:
            return None # not plottable

        name = chan.name + " (" + str(ctrl.seq_num) + ")"
        if self.ui.ckbPoint.isChecked():
            c = Curve(range(len(data)), data, Pen(self.color[i], 2), Symbol(Circle, Black, 4), name)
        else:
            c = Curve(range(len(data)), data, Pen(self.color[i], 2), name)
        return c


    def __acquire_data(self):
        # Initialize the list of curves to draw
        curves = []

        # If the user wants to display all the channels, then add all
        # curves to the list ...
        if self.ui.ckbNShow.isChecked():
            i = 0
            for chan in self.zdevlist[self.d_i].cset[self.cs_i].chan:
                if chan.is_interleaved():
                    continue; # skip interleaved
                curves.append(self.__acquire_chan(chan, i))
                i = i + 1
        # ... otherwise add only the selected channel's curve
        else:
            chan = self.zdevlist[self.d_i].cset[self.cs_i].chan[self.ch_i]
            curves.append(self.__acquire_chan(chan, self.ch_i))
        # Create a plot of curves
        p = Plot("Data")
        p.hide()
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

    def acquire_click(self):
        """Event associated to the click on the acquire button. When
        invoked, it acquires on all requested channel"""

        if self.d_i == None or self.cs_i == None or self.ch_i == None:
            print("Select channel before acquire")
            return


        if self.ui.ckbContinuous.isChecked():
            if self.ui.btnAcq.text() == "Acquire":
                self.ui.btnAcq.setText(QtGui.QApplication.translate("zGui", "Stop", None, QtGui.QApplication.UnicodeUTF8))
            else:
                self.ui.btnAcq.setText(QtGui.QApplication.translate("zGui", "Acquire", None, QtGui.QApplication.UnicodeUTF8))

            # TODO acquire data continous
        else:
            self.__acquire_data()


    def __refresh_attr_gui(self, tab, attrListGUI, attrs_list):
        """Remove old attributes and update the GUI with new ones"""
        x = 10
        y = 10
        del attrListGUI[:]
        for attr in attrs_list:
            attrListGUI.append(ZioAttributeGUI(self, tab, attrs_list[attr], x, y))
            y += 30

    def __get_name_list(self, zobjs):
        names = []
        for o in zobjs:
            names.append(o.name)
        return names

    def change_device(self, i):
        """Change selected device. It is the combo box handler for change index.
        The i parameter is used to select the device"""
        self.d_i = i
        # Update the cset combo box

        self.update_object_list(self.__get_name_list(self.zdevlist[self.d_i].cset), self.ui.cmbCset)
        self.__refresh_attr_gui(self.ui.tabDev, self.zdev_attr, self.zdevlist[self.d_i].attribute)


    def change_cset(self, i):
        """Change selected cset. It is the combo box handler for change index.
        The i parameter is used to select the cset"""
        self.cs_i = i
        # Update the channel combo box
        self.update_object_list(self.__get_name_list(self.zdevlist[self.d_i].cset[i].chan), self.ui.cmbChan)
        self.__refresh_attr_gui(self.ui.tabCset, self.cset_attr, self.zdevlist[self.d_i].cset[self.cs_i].attribute)

        # update buffer
        buf_name = self.zdevlist[self.d_i].cset[i].get_current_buffer()
        i = self.ui.cmbBuf.findText(buf_name)
        self.ui.cmbBuf.setCurrentIndex(i)
        if self.b_i == None:  # for initialization
            self.change_buffer(i)

        # update trigger
        trig_name = self.zdevlist[self.d_i].cset[self.cs_i].get_current_trigger()
        i = self.ui.cmbTrig.findText(trig_name)
        self.ui.cmbTrig.setCurrentIndex(i)
        if self.t_i == None:  # for initialization
            self.change_trigger(i)


    def change_buffer(self, i):
        """Change selected buffer. It is the combo box handler for change index.
        The i parameter is used to select the buffer"""
        if self.d_i == None or self.cs_i == None:
            print("Select channel set before change buffer")
            self.ui.cmbBuf.setCurrentIndex(0)
            return
        self.b_i = i
        text = self.ui.cmbBuf.itemText(self.b_i)
        self.zdevlist[self.d_i].cset[self.cs_i].set_current_buffer(text)
        print("Change Buffer to " + text)
        self.__refresh_attr_gui(self.ui.tabBuf, self.buf_attr, self.zdevlist[self.d_i].cset[self.cs_i].chan[self.ch_i].buffer.attribute)


    def change_trigger(self, i):
        """Change selected trigger. It is the combo box handler for change index.
        The i parameter is used to select the triger"""
        if self.d_i == None or self.cs_i == None:
            print("Select channel set before change trigger")
            self.ui.cmbTrig.setCurrentIndex(0)
            return
        self.t_i = i
        text = self.ui.cmbTrig.itemText(i)
        self.zdevlist[self.d_i].cset[self.cs_i].set_current_trigger(text)
        print("Change Trigger to " + text)
        self.__refresh_attr_gui(self.ui.tabTrig, self.trig_attr, self.zdevlist[self.d_i].cset[self.cs_i].trigger.attribute)


    def change_chan(self, i):
        """Change selected channel. It is the combo box handler for change index.
        The i parameter is used to select the channel"""
        self.ch_i = i
        self.__refresh_attr_gui(self.ui.tabChan, self.chan_attr, self.zdevlist[self.d_i].cset[self.cs_i].chan[i].attribute)
