#!/usr/bin/python

import sys
sys.path.append('../lib/Adafruit')
from Adafruit_PWM_Servo_Driver import PWM
import time

# The following quantities are in microseconds (us):
ZERO_THROTTLE = 530
FULL_THROTTLE = 1860

# Set channels
REAR_LEFT_MOTOR_CHANNEL = 11
FRONT_LEFT_MOTOR_CHANNEL = 15
REAR_RIGHT_MOTOR_CHANNEL = 7
FRONT_RIGHT_MOTOR_CHANNEL = 3

motors = [ REAR_LEFT_MOTOR_CHANNEL, REAR_RIGHT_MOTOR_CHANNEL, FRONT_LEFT_MOTOR_CHANNEL, FRONT_RIGHT_MOTOR_CHANNEL ]

# Adapted from https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_PWM_Servo_Driver

# Initialise the PWM device using the default address
pwm = PWM(0x40)
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

def set_motor(channel, pulse):
  pulseLength = 20000 
  pulseLength /= 4096                     # 12 bits of resolution
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

def config_motors():
    for m in motors:
        set_motor(m, FULL_THROTTLE)
        time.sleep(0.5)
    for m in motors:
        set_motor(m, ZERO_THROTTLE)
        time.sleep(0.5)

def cleanup():
    for m in motors:
        set_motor(m, 0)

config_motors()

while True:
    try:
        #print "1 = Rear Left Motor"
        #print "2 = Rear Right Motor"
        #print "4 = Front Left Motor"
        #print "8 = Front Right Motor"
        #m = int(raw_input('Enter motor number (or sum of multiple) or a non-integer to quit: '))
        #if m < 1 or m > 15:
        #    raise ValueError('Invalid motor selected')
        throttle_value_us = int(raw_input('Enter pulse length in microseconds (' + str(ZERO_THROTTLE) + ' - ' + str(FULL_THROTTLE) + ') or a non-integer to quit: '))
        #if throttle_value_us < ZERO_THROTTLE or throttle_value_us > FULL_THROTTLE:
        #    raise ValueError('Outside throttle range')
    except ValueError:
        print "Okay, stopping."
        break

    #print m, throttle_value_us
    #if m & 1:
    set_motor(REAR_LEFT_MOTOR_CHANNEL, throttle_value_us)
    #if m & 2:
    set_motor(REAR_RIGHT_MOTOR_CHANNEL, throttle_value_us)
    #if m & 4:
    set_motor(FRONT_LEFT_MOTOR_CHANNEL, throttle_value_us)
    #if m & 8:
    set_motor(FRONT_RIGHT_MOTOR_CHANNEL, throttle_value_us)

cleanup()
