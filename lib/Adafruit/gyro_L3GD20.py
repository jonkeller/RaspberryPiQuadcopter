#!/usr/bin/python

from Adafruit_L3GD20 import *

import time

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


if __name__ == '__main__':

    gyro = L3GD20()

    avgDrift = getAvgDrift(gyro)

    gyroXAngle = gyroYAngle = gyroZAngle = 0
    loopCnt = 0;

    lastTime = time.time() * 1000

    while True:

        readout = gyro.read()

        currentTime = time.time() * 1000
        timeDiff = currentTime - lastTime
        lastTime = currentTime

        gyroXAngle += (readout[0] - avgDrift[0]) * gyro.GAIN * (timeDiff / 1000)
        gyroYAngle += (readout[1] - avgDrift[1]) * gyro.GAIN * (timeDiff / 1000)
        gyroZAngle += (readout[2] - avgDrift[2]) * gyro.GAIN * (timeDiff / 1000)


        if (loopCnt > 0 and (loopCnt % 25) == 0):
            print 'X: ' + str(gyroXAngle) + ' Y: ' + str(gyroYAngle) + ' Z: ' + str(gyroZAngle)
            loopCnt = 0

        loopCnt += 1

        time.sleep(0.02)
