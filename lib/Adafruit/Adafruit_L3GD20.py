#!/usr/bin/python

from Adafruit_I2C import Adafruit_I2C

class L3GD20(Adafruit_I2C):

    L3GD20_ADDRESS = 0x6b
                                             # Default    Type
    L3GD20_REGISTER_CTRL_REG1 = 0x20         # 00000111   rw
    L3GD20_REGISTER_CTRL_REG4 = 0x23         # 00000000   rw

    L3GD20_REGISTER_OUT_X_L = 0x28

    GAIN = 0.07

    def __init__(self, busnum=-1, debug=False):

        self.gyro = Adafruit_I2C(self.L3GD20_ADDRESS, busnum, debug)

        self.gyro.write8(self.L3GD20_REGISTER_CTRL_REG1, 0x0F)
        self.gyro.write8(self.L3GD20_REGISTER_CTRL_REG4, 0x30)
  

    def gyro16(self, list, idx):
        n = (list[idx+1] << 8) | list[idx]
        return n if n < 32768 else n - 65536


    def read(self):
        list = self.gyro.readList(
          self.L3GD20_REGISTER_OUT_X_L | 0x80, 6)
        res = ( self.gyro16(list, 0),
                 self.gyro16(list, 2),
                 self.gyro16(list, 4) )

        return res
