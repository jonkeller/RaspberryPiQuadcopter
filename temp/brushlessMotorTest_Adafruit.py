#!/usr/bin/python

# From http://raspberrypi.stackexchange.com/questions/18254/can-i-control-this-esc-brushless-motor-with-a-raspberry-pi-and-or-arduino

from Adafruit_PWM_Servo_Driver import PWM
import time, curses

pwm = PWM(0x40, debug=True)
pwm.setPWMFreq(60)

screen = curses.initscr()

curses.noecho()
curses.cbreak()

screen.keypad(True)

running = True
fwdmax = 600
stop = 400
revmax = 200
go = 400
inc = 20
spinup = 1

def bootup():
    boot = 200
    while boot < fwdmax:
        boot += inc
        pwm.setPWM(0,0,boot)
        time.sleep(0.1)
        if boot > fwdmax:
            while boot > revmax:
                 boot -= inc
                 pwm.setPWM(0,0,boot)
                 time.sleep(0.1)
                 if boot < revmax:
                     boot = 400
                     pwm.setPWM(0,0,boot)
                     spinup = 0
                     break

while running:
        char = screen.getch()
        if char == ord('q'):
                running=False
        else:
                if char == ('b') and spinup == 1:
                    bootup()
                if char == curses.KEY_UP:
                        if go < fwdmax:
                                go += inc
                elif char == curses.KEY_DOWN:
                        if go > revmax:
                                go -= inc

                elif char == ord(' '):
                        go = stop
        pwm.setPWM(0, 0, go)
# shut down cleanly
curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()
