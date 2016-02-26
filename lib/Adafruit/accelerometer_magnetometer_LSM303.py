#!/usr/bin/python

from Adafruit_LSM303 import Adafruit_LSM303
from time import sleep

lsm = Adafruit_LSM303()

print '[(Accelerometer X, Y, Z), (Magnetometer X, Y, Z, orientation)]'
while True:
    print lsm.read()
    sleep(1) # Output is fun to watch if this is commented out
