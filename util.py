'''
Created on 12/mar/2012

@author: federico
'''
import os
import string
from zobject.device import zDev
from config import *


def getAttrIndex(zlist, name):
    try:
        i = zlist.index(name)
        return i
    except ValueError:
        return -1

def getAvailableBuffers():
    if not os.access(zio_bus_path + "/available_buffers", os.R_OK):
        print "ZIO is not loaded, missing available_buffers"
        exit()
    # read all available buffers
    f = open(zio_bus_path + "/available_buffers", "r")
    for line in f:
        buffers.append(line.rstrip('\n'))
    f.close()

def getAvailableTriggers():
    if not os.access(zio_bus_path + "/available_triggers", os.R_OK):
        print "ZIO is not loaded, missing available_triggers"
        exit()
    # read all available triggers
    f = open(zio_bus_path + "/available_triggers", "r")
    for line in f:
        triggers.append(line.rstrip('\n'))
    f.close()
def getAvailableDevices():
    for zdev in os.listdir(devices_path):
        prefix = string.find(zdev, "zio-")
        if prefix == -1:
            continue
        newDev = zDev(devices_path, zdev)
        devices.append(newDev)