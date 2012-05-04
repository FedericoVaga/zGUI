'''
Created on 24/feb/2012

@author: federico
'''

verbose = 0
stressLevel = 50
triggers = [] #list of available triggers (string)
buffers = [] # list of available buffers (string)
devices = [] # list of available devices (zdev object)
zio_cdev_path = "/dev/zio/"
zio_bus_path = "/sys/bus/zio"
devices_path = zio_bus_path + "/devices/"