#!/usr/bin/python

from RPIO import PWM
import time
import sys

servo = PWM.Servo()

SERVO_PIN = 8

def set_us_time(us):
    # Set servo on SERVO_PIN to 2000us (2.0ms)
    #servo.set_servo(SERVO_PIN, 1200)
    servo.set_servo(SERVO_PIN, us)

print "At any time, type something that isn't an integer to quit."
while True:
    try:
        us = int(raw_input('Enter num microseconds (560...1530...2500)? '))
    except ValueError:
        print "Okay, stopping."
        break

    try:
        set_us_time(us)
    except (RuntimeError, TypeError, NameError) as detail:
        print "Unexpected error:", detail
    except:
        print "Unexpected error:", sys.exc_info()[0]
        break

servo.stop_servo(SERVO_PIN)

