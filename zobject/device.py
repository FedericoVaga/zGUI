'''
Created on 27/feb/2012

@author: federico
'''
import os

from cset import zCset
import config
from attribute import zAttribute

class zDev(object):
    '''
    classdocs
    '''


    def __init__(self, path, name):
        '''
        Constructor
        '''
        if config.verbose == 1:
            print "Device found '" + name + "'"
        self.name = name
        self.path = path
        self.cset = []
        self.attribute = {}
        fullPath = os.path.join(path, name)
        for el in os.listdir(fullPath):
            if el == "power" or el == "driver" or el == "subsystem" or el == "uevent":
                continue
            if os.path.isdir(os.path.join(fullPath, el)):
                newCset = zCset(fullPath, el)
                self.cset.append(newCset)
            else:
                newAttr = zAttribute(fullPath, el)
                self.attribute[el] = newAttr
    
    def getCsetsName(self):
        names = []
        for cset in self.cset:
            names.append(cset.name)
        return names
    
    def refreshAttributes(self):
        for attr in self.attribute:
            self.attribute[attr].read()
        for cset in self.cset:
            cset.refreshAttributes()
    
    def isEnable(self):
        return self.attribute["enable"].read()
    def enable(self):
        self.attribute["enable"].write("1")
    def disable(self):
        self.attribute["enable"].write("0")