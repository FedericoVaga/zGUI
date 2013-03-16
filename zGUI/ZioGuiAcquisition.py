"""
@author: Federico Vaga
@copyright: Federico Vaga 2013
@license: GPLv2
"""

from PyZio.ZioChan import ZioChan
from PyZio.ZioCset import ZioCset
import os

class ZioGuiAcquisition(object):
    """
    This class handles the acquisition from the ZIO device
    """


    def __init__(self, zobj, stop_event, running_event, queue):
        """
        The constructor store the parameters within the object and it starts
        immediately the acquisition
        """
        self.zobj = zobj
        self.stop_ev = stop_event
        self.run_ev = running_event
        self.queue = queue

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


    def __flush_unread_queue(self):
        """
        This function flush the queue assigned to this process from the
        unread block. This is done when an acquisition is over and the consumer
        process did not read some blocks. The acquisition process cannot stop
        while the queue is not empty
        """
        try:
            while self.queue.get_nowait():
                pass
        except:
            pass


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
            print("[Error] Unknown object", self.zobj, ", cannot acquire")
            return

        self.run_ev.set()   # The acquisition start
        print("Start Acquisition")
        while True:
            self.queue.put(func(self.zobj))
            if self.stop_ev.is_set():
                self.flush_unread_queue()
                self.stop_ev.clear()
                break;
        print("End Acquisition")
        self.run_ev.clear() # The acquisition is over
