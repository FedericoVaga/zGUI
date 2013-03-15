"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

from PyQt4 import QtCore, QtGui

from PyQt4.Qwt5.qplt import Circle
from PyQt4.Qwt5.qplt import Plot, Pen, Curve, Symbol
from PyQt4.Qwt5.qplt import Black, Red, Yellow, Cyan, Magenta, Green, Blue

from PyZio import ZioUtil
from PyZio.ZioDev import ZioDev
from PyZio.ZioConfig import buffers, triggers, devices, devices_path
from zGUI.ZioAttributeGUI import ZioAttributeGUI

from multiprocessing import Process, Queue, Event
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class ZioGuiHandler(QtCore.QObject):
    dtry = QtCore.pyqtSignal(name = "ZioBlockReady")  # Data Ready signal
    zgui_color = [Red, Green, Blue, Black, Yellow, Cyan, Magenta]

    def __init__(self, ui):
        """It initialize the GUI and connect GUI events"""
        super(ZioGuiHandler, self).__init__()
        self.ui = ui
        self.zdevlist = []
        self.color_index = 0;
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

        # Create the queue of blocks to draw
        self.sample_queue = Queue()
        # Create the stop event
        self.running_event = Event()
        self.stop_event = Event()

        # Place the Plot Object in the GUI
        self.ui.graph = Plot(self.ui.centralwidget)
        self.ui.graph.setGeometry(QtCore.QRect(220, 10, 781, 381))
        self.ui.graph.setObjectName(_fromUtf8("graph"))

        # Configure Events
        self.ui.cmbDev.currentIndexChanged.connect(self.change_device)
        self.ui.cmbCset.currentIndexChanged.connect(self.change_cset)
        self.ui.cmbChan.currentIndexChanged.connect(self.change_chan)
        self.ui.cmbBuf.currentIndexChanged.connect(self.change_buffer)
        self.ui.cmbTrig.currentIndexChanged.connect(self.change_trigger)
        self.ui.btnAcq.clicked.connect(self.acquire_click)
        self.ui.actionExit.triggered.connect(exit)

        self.dtry.connect(self.__plot_curves)

        # Looks for devices
        self.refresh_device()


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

    def __acquire_chan(self, chan):
        """Acquire data from channel and draw its curve"""
        chan.interface.open_ctrl_data(os.O_RDONLY)
        ctrl, data = chan.interface.read_block(True, True)
        chan.interface.close_ctrl_data()
        if ctrl == None or data == None:
            return None # not plottable
        return chan, ctrl, data


    def __acquire_data(self):
        # Initialize the list of curves to draw
        blocks = []

        # If the user wants to display all the channels, then add all
        # curves to the list ...
        if self.ui.ckbNShow.isChecked():
            i = 0
            for chan in self.zdevlist[self.d_i].cset[self.cs_i].chan:
                if chan.is_interleaved():
                    continue; # skip interleaved
                blocks.append(self.__acquire_chan(chan))
                i = i + 1
        # ... otherwise add only the selected channel's curve
        else:
            chan = self.zdevlist[self.d_i].cset[self.cs_i].chan[self.ch_i]
            blocks.append(self.__acquire_chan(chan))

        return blocks


    def __plot_curves(self):
        """It plots given curves into the user interface"""

        self.ui.graph.clear()
        blocks = self.sample_queue.get()
        for chan, ctrl, data in blocks:
            name = chan.name + " (" + str(ctrl.seq_num) + ")"
            if self.ui.ckbPoint.isChecked():
                c = Curve(range(len(data)), data, Pen(self.zgui_color[1], 2), \
                          Symbol(Circle, Black, 4), name)
            else:
                c = Curve(range(len(data)), data, Pen(self.zgui_color[1], 2), \
                          name)

            if c == None:
                print("Cannot plot None")
                continue
            self.ui.graph.plot(c)


    def __process_acquisition(self, stop_event, running_event, queue):
        """This function is an indipendent process which update the chart
        content."""
        running_event.set()
        i = 0
        while True:
            i = i + 1
            blocks = self.__acquire_data()
            queue.put(blocks)
            # FIXME this signal emission does not work
            # self.dtry.emit()  # Send data ready signal
            if stop_event.is_set():
                stop_event.clear()
                running_event.clear()
                break


    def acquire_click(self):
        """Event associated to the click on the acquire button. When
        invoked, it acquires on all requested channel"""
        if self.d_i == None or self.cs_i == None or self.ch_i == None:
            print("Select channel before acquire")
            return

        is_streaming = self.ui.ckbContinuous.isChecked()

        if not self.running_event.is_set():  # If not running, then start
            self.p = Process(target = self.__process_acquisition, \
                             name = "acquisition", \
                             args = (self.stop_event, self.running_event, \
                                     self.sample_queue)
                             )
            self.p.start()

            if is_streaming:  # If is streaming change the button label to Stop
                self.ui.btnAcq.setText(QtGui.QApplication.translate("zGui", \
                            "Stop", None, QtGui.QApplication.UnicodeUTF8))
                self.ui.ckbContinuous.setDisabled(True)
            else:  # If is not streaming, then
                self.stop_event.set()  # Single shot, stop acquisition process

        elif is_streaming:  # acquisition process already running streaming
            self.stop_event.set()  # Stop acquisition (Stop button pressed)
            self.ui.btnAcq.setText(QtGui.QApplication.translate("zGui", \
                            "Acquire", None, QtGui.QApplication.UnicodeUTF8))
            self.ui.ckbContinuous.setDisabled(False)
        else:  # acquisition process is running a single shot
            print("Congratulation, you are faster than acquisition. Try Later")
            return  # nothing to do


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
