'''
Created on 27/feb/2012

@author: federico
'''
import os
from attribute import zAttribute
from config import *
from buffer import zBuf
from control import zCtrl
from data import zData
from stat import ST_MODE

class zChan(object):
    '''
    classdocs
    '''
    def __init__(self, path, name):
        '''
        Constructor
        '''
        if verbose == 1:
            print "Found Channel '" + name + "'"
        self.name = name
        self.path = path
        self.curctrl = None
        self.buffer = None
        self.attribute = {}
        fullPath = os.path.join(path, name)
        for el in os.listdir(fullPath):
            if el == "power" or el == "driver" or el == "subsystem" or el == "uevent":
                continue
            if el == "buffer":
                self.buffer = zBuf(fullPath, el)
                continue
            if el == "current_control":
                self.curctrl = zCtrl(fullPath, el)
            newAttr = zAttribute(fullPath, el)
            self.attribute[el] = newAttr
        # Set if this channel is for input or output
        zmode = oct(os.stat(zio_cdev_path + "zio-zzero-0000-0-1-ctrl")[ST_MODE])[-3:]
        self.isOutput = True if zmode == 222 else False
        # Set source for control and data
        self.ctrlcdev = zCtrl(zio_cdev_path, "zio-zzero-0000-0-1-ctrl")
        self.datacdev = zData(zio_cdev_path, "zio-zzero-0000-0-1-data", self.ctrlcdev)
        
    def refreshAttributes(self):
        for attr in self.attribute:
            self.attribute[attr].read()
        self.buffer.refreshAttributes()
    
    def refreshBuffer(self):
        fullPath = os.path.join(self.path, self.name)
        self.buffer = zBuf(fullPath, "buffer")

    def isEnable(self):
        return self.attribute["enable"].read()
    def enable(self):
        self.attribute["enable"].write("1")
    def disable(self):
        self.attribute["enable"].write("0")