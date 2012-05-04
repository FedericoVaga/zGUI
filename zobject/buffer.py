'''
Created on 27/feb/2012

@author: federico
'''
import os
from config import *
from attribute import zAttribute

class zBuf(object):
    '''
    classdocs
    '''
    def __init__(self, path, name):
        '''
        Constructor
        '''
        if verbose == 1:
            print "Found Buffer"
        self.name = name
        self.path = path
        self.attribute = {}
        self.__fetchAttributes()
    
    def __fetchAttributes(self):
        fullPath = os.path.join(self.path, self.name)
        for el in os.listdir(fullPath):
            if el == "power" or el == "driver" or el == "subsystem" or el == "uevent":
                continue
            newAttr = zAttribute(fullPath, el)
            self.attribute[el] = newAttr
    
    def refreshAttributes(self):
        for attr in self.attribute:
            self.attribute[attr].read()