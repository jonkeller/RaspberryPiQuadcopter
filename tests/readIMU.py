#!/usr/bin/python

# Adapted from:
# https://github.com/darevish/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_L3GD20
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_LSM303
# https://github.com/adafruit/Adafruit_Python_BMP

import sys
import time
from smbus import SMBus
from ctypes import c_short
sys.path.append('../lib/Adafruit')
from Adafruit_L3GD20 import *
from Adafruit_LSM303 import Adafruit_LSM303

def readAccelerometerAndMagnetometer(lsm):
    print '[(Accelerometer X, Y, Z), (Magnetometer X, Y, Z, orientation)]'
    print lsm.read()


def getAvgDrift(gyro):
    print 'getAvgDrift begin'
    gyroXAngle = gyroYAngle = gyroZAngle = 0
    sampleCnt = 500

    for i in range(0, sampleCnt):
        readout = gyro.read()
        gyroXAngle += readout[0]
        gyroYAngle += readout[1]
        gyroZAngle += readout[2]
        time.sleep(0.02)

    print 'getAvgDrift end'
        
    return (
        gyroXAngle / sampleCnt,
        gyroYAngle / sampleCnt,
        gyroZAngle / sampleCnt
    )

def readGyro(gyro):
    gyroXAngle = gyroYAngle = gyroZAngle = 0
    #loopCnt = 0;
    lastTime = time.time() * 1000
    #while True:
    readout = gyro.read()
    currentTime = time.time() * 1000
    timeDiff = currentTime - lastTime
    lastTime = currentTime

    gyroXAngle += (readout[0] - avgDrift[0]) * gyro.GAIN * (timeDiff / 1000)
    gyroYAngle += (readout[1] - avgDrift[1]) * gyro.GAIN * (timeDiff / 1000)
    gyroZAngle += (readout[2] - avgDrift[2]) * gyro.GAIN * (timeDiff / 1000)

    #if (loopCnt > 0 and (loopCnt % 25) == 0):
    print 'X: ' + str(gyroXAngle) + ' Y: ' + str(gyroYAngle) + ' Z: ' + str(gyroZAngle)
    #    loopCnt = 0

    #loopCnt += 1

    #time.sleep(0.02)

# return two bytes from data as a signed 16-bit value
def get_short(data, index):
        return c_short((data[index] << 8) + data[index + 1]).value

# return two bytes from data as an unsigned 16-bit value
def get_ushort(data, index):
        return (data[index] << 8) + data[index + 1]

def readTemperatureAndPressure(addr, bus):
    oversampling = 3        # 0..3

    (chip_id, version) = bus.read_i2c_block_data(addr, 0xD0, 2)
    print "Chip Id:", chip_id, "Version:", version

    print "Reading calibration data..."
    # Read whole calibration EEPROM data
    cal = bus.read_i2c_block_data(addr, 0xAA, 22)

    # Convert byte data to word values
    ac1 = get_short(cal, 0)
    ac2 = get_short(cal, 2)
    ac3 = get_short(cal, 4)
    ac4 = get_ushort(cal, 6)
    ac5 = get_ushort(cal, 8)
    ac6 = get_ushort(cal, 10)
    b1 = get_short(cal, 12)
    b2 = get_short(cal, 14)
    mb = get_short(cal, 16)
    mc = get_short(cal, 18)
    md = get_short(cal, 20)

    print "Starting temperature conversion..."
    bus.write_byte_data(addr, 0xF4, 0x2E)
    time.sleep(0.005)
    (msb, lsb) = bus.read_i2c_block_data(addr, 0xF6, 2)
    ut = (msb << 8) + lsb

    print "Starting pressure conversion..."
    bus.write_byte_data(addr, 0xF4, 0x34 + (oversampling << 6))
    time.sleep(0.04)
    (msb, lsb, xsb) = bus.read_i2c_block_data(addr, 0xF6, 3)
    up = ((msb << 16) + (lsb << 8) + xsb) >> (8 - oversampling)

    print "Calculating temperature..."
    x1 = ((ut - ac6) * ac5) >> 15
    x2 = (mc << 11) / (x1 + md)
    b5 = x1 + x2 
    t = (b5 + 8) >> 4

    print "Calculating pressure..."
    b6 = b5 - 4000
    b62 = b6 * b6 >> 12
    x1 = (b2 * b62) >> 11
    x2 = ac2 * b6 >> 11
    x3 = x1 + x2
    b3 = (((ac1 * 4 + x3) << oversampling) + 2) >> 2

    x1 = ac3 * b6 >> 13
    x2 = (b1 * b62) >> 16
    x3 = ((x1 + x2) + 2) >> 2
    b4 = (ac4 * (x3 + 32768)) >> 15
    b7 = (up - b3) * (50000 >> oversampling)

    p = (b7 * 2) / b4
    #p = (b7 / b4) * 2

    x1 = (p >> 8) * (p >> 8)
    x1 = (x1 * 3038) >> 16
    x2 = (-7357 * p) >> 16
    p = p + ((x1 + x2 + 3791) >> 4)

    print
    print "Temperature:", t/10.0, "C"
    print "Pressure:", p / 100.0, "hPa"

lsm = Adafruit_LSM303()
gyro = L3GD20()

print "=== Gyro ==="
avgDrift = getAvgDrift(gyro)
readGyro(gyro)

print "=== Accelerometer and Magnetometer ==="
readAccelerometerAndMagnetometer(lsm)

print "=== Temperature ==="
addr_bmp180 = 0x77
bus = SMBus(1);         # 0 for R-Pi Rev. 1, 1 for Rev. 2
readTemperatureAndPressure(addr_bmp180, bus)

