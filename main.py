#!/usr/bin/python

import sys
import time
#from ctypes import c_short
sys.path.append('lib/Adafruit')
#from Adafruit_L3GD20 import *
#from Adafruit_LSM303 import Adafruit_LSM303

class Drone:
    done = False

    def __init__(self):
        pass

    def mainLoop(self):
        while not self.done:
            self.sense()
            self.move()

    def sense(self):
        print "Sense"

    def move(self):
        print "Move"

drone = Drone()
drone.mainLoop()

