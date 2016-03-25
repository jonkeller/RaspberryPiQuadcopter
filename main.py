#!/usr/bin/python

import sys
import time
#from ctypes import c_short
sys.path.append('lib/Adafruit')
#from Adafruit_L3GD20 import *
#from Adafruit_LSM303 import Adafruit_LSM303

done = False

def init():
    pass

def mainLoop():
    while not done:
        sense()
        move()

def sense():
    print "Sense"

def move():
    print "Move"

init()
mainLoop()

