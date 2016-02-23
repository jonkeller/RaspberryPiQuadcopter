#!/usr/bin/python
# Adapted from: http://withr.me/let-rpi-drive-brushless-motor/

import sys
from RPIO import PWM

if 2 != len(sys.argv):
    print "Please supply one argument: the pin number of the motor."
    exit(0)

SERVO_PIN = int(sys.argv[1])
print "Testing motor on pin:", SERVO_PIN
FULL_THROTTLE = 1860
ZERO_THROTTLE = 530

servo = PWM.Servo()

# TODO: Is this even necessary?
def config():
    servo.set_servo(SERVO_PIN, FULL_THROTTLE)
    raw_input('Now connect the power to the ESC, and press Enter...')
    servo.set_servo(SERVO_PIN, ZERO_THROTTLE)
    

while True:
    try:
        throttle_value_us = int(raw_input('Enter pulse length in microseconds (' + str(ZERO_THROTTLE) + ' - ' + str(FULL_THROTTLE) + ') or a non-integer to quit: '))
        if throttle_value_us < ZERO_THROTTLE or throttle_value_us > FULL_THROTTLE:
            raise ValueError('Outside throttle range')
    except ValueError:
        print "Okay, stopping."
        break

    servo.set_servo(SERVO_PIN, throttle_value_us)

servo.stop_servo(SERVO_PIN)
