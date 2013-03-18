"""
@author: Federico Vaga
@copyright: Federico Vaga 2013
@license: GPLv2
"""

from PyZio.ZioChan import ZioChan
from PyZio.ZioCset import ZioCset

from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal
import os

class ZioGuiAcquisition(QtCore.QThread):
    """
    This class handles the acquisition from the ZIO device. This class inherit
    from QThread so, you must run this class as an independent thread.

    This is a producer thread and it communitates to its consumer that a
    block is ready with the data_ready signal. Consumers of this class can
    connect an handler to this signal to get informed when a block is ready to
    be consumed.
    """

    data_ready = pyqtSignal(name = "BlockReady")

    def __init__(self, zobj, stop_event, queue, parent = None):
        """
        The constructor store the parameters within the object and it starts
        immediately the acquisition
        """
        QtCore.QThread.__init__(self, parent)

        self.zobj = None
        self.stop_ev = stop_event
        self.queue = queue


    def set_zobject(self, zobj):
        self.zobj = zobj


    def run(self):
        self.__process_acquisition()


    def __acquire_chan_block(self, chan):
        """
        Acquire data from channel and it returns a list of one block. The
        function returns a list to be compatible with the function
        acquire_cset_blocks(), so another object can use the result in the
        same way
        """
        chan.interface.open_ctrl_data(os.O_RDONLY)
        ctrl, data = chan.interface.read_block(True, True)
        chan.interface.close_ctrl_data()
        if ctrl == None or data == None:
            return None # not plottable

        return [(chan, ctrl, data), ]


    def __acquire_cset_blocks(self, cset):
        """
        Acquire data from channel set and it returns a list of blocks
        """
        blocks = []

        for chan in cset.chan:
            if chan.is_interleaved():
                continue; # skip interleaved
            blocks.extend(self.__acquire_chan_block(chan))

        return blocks


    def __process_acquisition(self):
        """
        This function handle both case: streaming and one shot. Depending on
        the kind of instance of the parameter 'zobj' it performs an acquisition
        on a single channel or on all channel within a channel set. If 'zobj'
        is a ZioCset instance, then it performs an acquisition on the whole
        channel set; if 'zobj' is a ZioChan instance, then it performs an
        acquisition only on the given channel.

        The acquisition starts in a infinite loop; this loop end when a stop
        event is raised. In a single shot acquisition this event is always on,
        so it acquires only a single block and it returns immediately. In a
        streaming acquisition, it continues the acquisition until some one
        raise the stop event.
        """
        if isinstance(self.zobj, ZioCset):
            func = self.__acquire_cset_blocks
        elif isinstance(self.zobj, ZioChan):
            func = self.__acquire_chan_block
        else:
            print("[zGui Acquisition thread][Error] Unknown object" + \
                  str(self.zobj) + ", cannot acquire")
            return

        print("[zGui Acquisition thread] Start Acquisition")
        acquire = True
        i = 0
        while acquire:
            i = i + 1
            print("[zGui Acquisition thread] Acquisition " + str(i))
            self.queue.put(func(self.zobj))     # Put a block in the queue
            if self.stop_ev.is_set():           # Check is it must stop
                print("[zGui Acquisition thread] Acquisition " + str(i) + " stopped")
                self.stop_ev.clear()                # Clear stop flag
                acquire = False                     # Acquisition must stop
            print("[zGui Acquisition thread] Data Ready " + str(i) + " Signal")
            self.data_ready.emit()              # Send Data Ready signal
        print("[zGui Acquisition thread] End Acquisition")
