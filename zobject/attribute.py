'''
Created on 27/feb/2012

@author: federico
'''

import os
from config import *

class zAttribute(object):
    '''
    classdocs
    '''
    def __init__(self, path, name):
        '''
        Constructor
        '''
        if verbose == 1:
            print "Found Attribute '" + name + "'"
        self.name = name
        self.path = path
        self .value = self.__read(os.path.join(path, name))
        
        if os.access(os.path.join(path, name), os.R_OK):
            self.readable = True
        else:
            self.readable = False
        
        if os.access(os.path.join(path, name), os.W_OK):
            self.writable = True
        else:
            self.writable = False

    def read(self):
        self.value = self.__read(os.path.join(self.path, self.name))
        return self.value
        pass

    def write(self, val):
        err = self.__write(os.path.join(self.path, self.name), val)
        if err != -1:
            self.value = val
        pass

    def __read(self, path):
        f = open(path, "r")
        val = f.read().rstrip("\n\r")
        f.close()
        return val

    # write a sysfs attriubute
    def __write(self, path, val):
        w = str(val)
        f = open(path, "w")
        f.write(w)
        self.read()
        pass