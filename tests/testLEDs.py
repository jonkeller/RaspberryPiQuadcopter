#!/usr/bin/python

import sys
sys.path.append('../lib/Adafruit')
from Adafruit_PWM_Servo_Driver import PWM
import time

# Set channels
FRONT_LEFT_LED = 12
FRONT_RIGHT_LED = 0
REAR_LEFT_LED = 8
REAR_RIGHT_LED = 4

# Adapted from https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_PWM_Servo_Driver

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

ledMin = 1  # Min pulse length out of 4096
ledMax = 4094  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

for channel in [FRONT_LEFT_LED, FRONT_RIGHT_LED, REAR_LEFT_LED, REAR_RIGHT_LED]:
  pwm.setPWM(channel, 0, 1)

while (True):
  # Change speed of continuous servo on channel O
  for channel in [FRONT_LEFT_LED, FRONT_RIGHT_LED, REAR_LEFT_LED, REAR_RIGHT_LED]:
      pwm.setPWM(channel, 0, ledMin)
      time.sleep(1)
  for channel in [FRONT_LEFT_LED, FRONT_RIGHT_LED, REAR_LEFT_LED, REAR_RIGHT_LED]:
      pwm.setPWM(channel, 0, ledMax)
      time.sleep(1)


