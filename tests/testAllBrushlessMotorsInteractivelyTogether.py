#!/usr/bin/python
# Adapted from: http://withr.me/let-rpi-drive-brushless-motor/

import time
from RPIO import PWM

# The following quantities are in microseconds (us):
ZERO_THROTTLE = 530
FULL_THROTTLE = 1860
GRANULARITY = 10

REAR_LEFT_MOTOR_PIN = 24 
FRONT_LEFT_MOTOR_PIN = 25
REAR_RIGHT_MOTOR_PIN = 18
FRONT_RIGHT_MOTOR_PIN = 23

motors = [ REAR_LEFT_MOTOR_PIN, REAR_RIGHT_MOTOR_PIN, FRONT_LEFT_MOTOR_PIN, FRONT_RIGHT_MOTOR_PIN ]

servo = PWM.Servo()

def config_motors():
    for m in motors:
        set_motor(m, FULL_THROTTLE)
        time.sleep(0.5)
    for m in motors:
        set_motor(m, ZERO_THROTTLE)
        time.sleep(0.5)
#    for m in motors:
#        set_motor(m, FULL_THROTTLE)
#        time.sleep(0.5)

def cleanup():
    for m in motors:
        servo.stop_servo(m)

def set_motor(m, us):
    us -= us % GRANULARITY
    servo.set_servo(m, us)

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
    set_motor(REAR_LEFT_MOTOR_PIN, throttle_value_us)
    #if m & 2:
    set_motor(REAR_RIGHT_MOTOR_PIN, throttle_value_us)
    #if m & 4:
    set_motor(FRONT_LEFT_MOTOR_PIN, throttle_value_us)
    #if m & 8:
    set_motor(FRONT_RIGHT_MOTOR_PIN, throttle_value_us)

cleanup()
