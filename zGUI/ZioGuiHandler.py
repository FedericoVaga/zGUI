"""
@author: Federico Vaga
@copyright: Federico Vaga 2012
@license: GPLv2
"""

from PyQt4 import QtCore
from PyQt4.QtGui import QApplication

from PyQt4.Qwt5.qplt import Circle
from PyQt4.Qwt5.qplt import Plot, Pen, Curve, Symbol
from PyQt4.Qwt5.qplt import Black, Red, Yellow, Cyan, Magenta, Green, Blue

from PyZio import ZioUtil
from PyZio.ZioDev import ZioDev
from PyZio.ZioConfig import buffers, triggers, devices, devices_path
from zGUI.ZioAttributeGUI import ZioAttributeGUI
from zGUI.ZioGuiAcquisition import ZioGuiAcquisition

from multiprocessing import Process, Queue, Event

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class ZioGuiHandler(QtCore.QObject):
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

        self.device = None
        self.channel_set = None
        self.channel = None
        self.trigger = None
        self.buffer = None

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


    def acquire_click(self):
        """Event associated to the click on the acquire button. When
        invoked, it acquires on all requested channel"""
        if self.device == None or self.channel_set == None or self.channel == None:
            print("Select channel before acquire")
            return

        is_streaming = self.ui.ckbContinuous.isChecked()
        if not self.running_event.is_set():  # If not running, then start
            zobj = self.channel_set if self.ui.ckbNShow.isChecked() \
                                    else self.channel

            self.p = Process(target = ZioGuiAcquisition, \
                             name = "acquisition", \
                             args = (zobj, self.stop_event, \
                                     self.running_event, self.sample_queue)
                             )

            if is_streaming:  # If is streaming, change button label to Stop
                self.ui.btnAcq.setText(QApplication.translate("zGui", "Stop", \
                                            None, QApplication.UnicodeUTF8))
                self.ui.ckbContinuous.setDisabled(True)
            else:                       # If is not streaming
                self.stop_event.set()   # stop acquisition after first block

            self.p.start()  # Start acquisition process

        elif is_streaming:  # acquisition process already running streaming
            self.stop_event.set()   # Stop acquisition (Stop button pressed)
            self.p.join()           # Wait the end of the process

            self.ui.btnAcq.setText(QApplication.translate("zGui", "Acquire", \
                                            None, QApplication.UnicodeUTF8))
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
        self.device = self.zdevlist[i]

        # Update the cset combo box
        self.update_object_list(self.__get_name_list(self.device.cset), \
                                self.ui.cmbCset)
        self.__refresh_attr_gui(self.ui.tabDev, self.zdev_attr, \
                                self.device.attribute)


    def change_cset(self, i):
        """Change selected cset. It is the combo box handler for change index.
        The i parameter is used to select the cset"""
        self.channel_set = self.device.cset[i]
        # Update the channel combo box

        self.update_object_list(self.__get_name_list(self.channel_set.chan), \
                                self.ui.cmbChan)
        self.__refresh_attr_gui(self.ui.tabCset, self.cset_attr, \
                                self.channel_set.attribute)

        # update buffer
        buf_name = self.channel_set.get_current_buffer()
        i = self.ui.cmbBuf.findText(buf_name)
        self.ui.cmbBuf.setCurrentIndex(i)
        if self.buffer == None:  # for initialization
            self.change_buffer(i)

        # update trigger
        trig_name = self.channel_set.get_current_trigger()
        i = self.ui.cmbTrig.findText(trig_name)
        self.ui.cmbTrig.setCurrentIndex(i)
        if self.trigger == None:  # for initialization
            self.change_trigger(i)


    def change_buffer(self, i):
        """Change selected buffer. It is the combo box handler for change
        index. The i parameter is used to select the buffer"""
        if self.device == None or self.channel_set == None or self.channel == None:
            print("Select channel set before change buffer")
            self.ui.cmbBuf.setCurrentIndex(0)
            return

        text = self.ui.cmbBuf.itemText(i)
        self.channel_set.set_current_buffer(text)
        self.buffer = self.channel.buffer

        print("Change Buffer to " + text)
        self.__refresh_attr_gui(self.ui.tabBuf, self.buf_attr, \
                                self.buffer.attribute)


    def change_trigger(self, i):
        """Change selected trigger. It is the combo box handler for change
        index. The i parameter is used to select the trigger"""
        if self.device == None or self.channel_set == None:
            print("Select channel set before change trigger")
            self.ui.cmbTrig.setCurrentIndex(0)
            return

        text = self.ui.cmbTrig.itemText(i)
        self.channel_set.set_current_trigger(text)
        self.trigger = self.channel_set.trigger

        print("Change Trigger to " + text)
        self.__refresh_attr_gui(self.ui.tabTrig, self.trig_attr, \
                                self.trigger.attribute)


    def change_chan(self, i):
        """Change selected channel. It is the combo box handler for change
        index. The i parameter is used to select the channel"""
        self.channel = self.channel_set.chan[i]
        self.__refresh_attr_gui(self.ui.tabChan, self.chan_attr, \
                                self.channel.attribute)
