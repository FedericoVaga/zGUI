'''
Created on 27/feb/2012

@author: federico
'''
import os
from channel import zChan
from trigger import zTrig
from attribute import zAttribute
from config import *

class zCset(object):
    '''
    classdocs
    '''
    def __init__(self, path, name):
        '''
        Constructor
        '''
        if verbose == 1:
            print "cset found '" + name + "'"
        self.name = name
        self.path = path
        self.chan = []
        self.trigger = None
        self.attribute = {}
        fullPath = os.path.join(path, name)
        for el in os.listdir(fullPath):
            if el == "power" or el == "driver" or el == "subsystem" or el == "uevent":
                continue
            if el == "trigger":
                self.trigger = zTrig(fullPath, el)
                continue
            
            if os.path.isdir(os.path.join(fullPath, el)):
                newChan = zChan(fullPath, el)
                self.chan.append(newChan)
            else:
                newAttr = zAttribute(fullPath, el)
                self.attribute[el] = newAttr

    def getChansName(self):
        names = []
        for chan in self.chan:
            names.append(chan.name)
        return names
    
    def refreshAttributes(self):
        for attr in self.attribute:
            self.attribute[attr].read()
        for chan in self.chan:
            chan.refreshAttributes()
        self.trigger.refreshAttributes()
    
    def getCurrentBuffer(self):
        return self.attribute["current_buffer"].read()
    def setCurrentBuffer(self, bufType):
        if verbose == 1:
            print "Buffer changed to " + bufType
        self.attribute["current_buffer"].write(bufType)
        for chan in self.chan:
            chan.refreshBuffer();
    
    def getCurrentTrigger(self):
        return self.attribute["current_trigger"].read()
    def setCurrentTrigger(self, trigType):
        if verbose == 1:
            print "Trigger changed to " + trigType
        self.attribute["current_trigger"].write(trigType)
        fullPath = self.trigger.path;
        self.trigger = zTrig(fullPath, "trigger")
    
    def isEnable(self):
        return self.attribute["enable"].read()
    def enable(self):
        self.attribute["enable"].write("1")
    def disable(self):
        self.attribute["enable"].write("0")