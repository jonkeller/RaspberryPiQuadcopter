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
    for m in motors:
        set_motor(m, FULL_THROTTLE)
        time.sleep(0.5)

def cleanup():
    for m in motors:
        servo.stop_servo(m)

def set_motor(m, us):
    us -= us % GRANULARITY
    servo.set_servo(m, us)

config_motors()

for m in motors:
    set_motor(m, (ZERO_THROTTLE + FULL_THROTTLE) / 2)

time.sleep(3)

cleanup()
