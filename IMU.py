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

# return two bytes from data as a signed 16-bit value
def get_short(data, index):
        return c_short((data[index] << 8) + data[index + 1]).value

# return two bytes from data as an unsigned 16-bit value
def get_ushort(data, index):
        return (data[index] << 8) + data[index + 1]

# A facade for a Gyro, Accelerometer, Magnetometer, Temperature Sensor, and Pressure Sensor
class IMU:
    lsm = None
    gyro = None
    addr_bmp180 = None
    bus = None

    gyroXAngle = 0
    gyroYAngle = 0
    gyroZAngle = 0
    accelerometerX = 0
    accelerometerY = 0
    accelerometerZ = 0
    magnetometerX = 0
    magnetometerY = 0
    magnetometerZ = 0
    orientation = 0
    temperature = 0.0
    pressure = 0.0

    def __init__(self):
        self.lsm = Adafruit_LSM303()
        self.gyro = L3GD20()
        (self.gyroXAngle, self.gyroYAngle, self.gyroZAngle) = getAvgDrift()
        self.addr_bmp180 = 0x77
        self.bus = SMBus(1); # 0 for R-Pi Rev. 1, 1 for Rev. 2

    def read(self):
        self.readGyro()
        self.readAccelerometerAndMagnetometer()
        self.readTemperatureAndPressure()

    def readGyro(self):
        lastTime = time.time() * 1000
        readout = self.gyro.read()
        currentTime = time.time() * 1000
        timeDiff = currentTime - lastTime
        lastTime = currentTime

        self.gyroXAngle += (readout[0] - avgDrift[0]) * self.gyro.GAIN * (timeDiff / 1000)
        self.gyroYAngle += (readout[1] - avgDrift[1]) * self.gyro.GAIN * (timeDiff / 1000)
        self.gyroZAngle += (readout[2] - avgDrift[2]) * self.gyro.GAIN * (timeDiff / 1000)

    def readAccelerometerAndMagnetometer(self):
        [acc, mag] = self.lsm.read()
        (self.accelerometerX, self.accelerometerY, self.accelerometerZ) = acc;
        (self.magnetometerX, self.magnetometerY, self.magnetometerZ, self.orientation) = mag;

    def readTemperatureAndPressure(self):
        oversampling = 3 # 0..3

        (chip_id, version) = self.bus.read_i2c_block_data(self.addr_bmp180, 0xD0, 2)

        # Read whole calibration EEPROM data
        cal = self.bus.read_i2c_block_data(self.addr_bmp180, 0xAA, 22)

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

        self.bus.write_byte_data(self.addr_bmp180, 0xF4, 0x2E)
        time.sleep(0.005)
        (msb, lsb) = self.bus.read_i2c_block_data(self.addr_bmp180, 0xF6, 2)
        ut = (msb << 8) + lsb

        self.bus.write_byte_data(self.addr_bmp180, 0xF4, 0x34 + (oversampling << 6))
        time.sleep(0.04)
        (msb, lsb, xsb) = self.bus.read_i2c_block_data(self.addr_bmp180, 0xF6, 3)
        up = ((msb << 16) + (lsb << 8) + xsb) >> (8 - oversampling)

        x1 = ((ut - ac6) * ac5) >> 15
        x2 = (mc << 11) / (x1 + md)
        b5 = x1 + x2 
        t = (b5 + 8) >> 4

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

        x1 = (p >> 8) * (p >> 8)
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * p) >> 16
        p = p + ((x1 + x2 + 3791) >> 4)

        self.temperature = t/10.0
        self.pressure = p/100.0

    def getAvgDrift():
        self.gyroXAngle = self.gyroYAngle = self.gyroZAngle = 0
        sampleCnt = 500

        for i in range(0, sampleCnt):
            readout = self.gyro.read()
            self.gyroXAngle += readout[0]
            self.gyroYAngle += readout[1]
            self.gyroZAngle += readout[2]
            time.sleep(0.02)

        self.gyroXAngle /= sampleCnt
        self.gyroYAngle /= sampleCnt
        self.gyroZAngle /= sampleCnt
