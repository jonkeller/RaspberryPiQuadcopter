#!/usr/bin/python
# Credit: http://withr.me/let-rpi-drive-brushless-motor/

from RPIO import PWM
s = PWM.Servo()
s.set_servo(4, 2000)
# Now connect the power to the ESC
s.set_servo(4, 1000)
s.set_servo(4, 1300)

