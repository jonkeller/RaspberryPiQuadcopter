#!/usr/bin/python
# Adapted from: http://withr.me/let-rpi-drive-brushless-motor/

from RPIO import PWM

SERVO_PIN = 4
FULL_THROTTLE = 2000
ZERO_THROTTLE = 1000

servo = PWM.Servo()
servo.set_servo(SERVO_PIN, FULL_THROTTLE)

raw_input('Now connect the power to the ESC, and press Enter...')

servo.set_servo(SERVO_PIN, ZERO_THROTTLE)
while True:
    try:
        us = int(raw_input('Enter num microseconds (' + str(ZERO_THROTTLE) + ' - ' + str(FULL_THROTTLE) + ') or a non-integer to quit: '))
    except ValueError:
        print "Okay, stopping."
        break
    if us < ZERO_THROTTLE or us > FULL_THROTTLE:
        print "Okay, stopping."
        break

    servo.set_servo(SERVO_PIN, ZERO_THROTTLE)

servo.stop_servo(SERVO_PIN)
