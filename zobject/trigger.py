'''
Created on 27/feb/2012

@author: federico
'''
import os
from attribute import zAttribute
from config import *

class zTrig(object):
    '''
    classdocs
    '''

    def __init__(self, path, name):
        '''
        Constructor
        '''
        if verbose == 1:
            print "Found trigger"
        self.name = name
        self.path = path
        self.attribute = {}
        fullPath = os.path.join(path, name)
        for el in os.listdir(fullPath):
            if el == "power" or el == "driver" or el == "subsystem" or el == "uevent":
                continue
            newAttr = zAttribute(fullPath, el)
            self.attribute[el] = newAttr
    
    def refreshAttributes(self):
        for attr in self.attribute:
            self.attribute[attr].read()
    
    def isEnable(self):
        return self.attribute["enable"].read()
    def enable(self):
        self.attribute["enable"].write("1")
    def disable(self):
        self.attribute["enable"].write("0")