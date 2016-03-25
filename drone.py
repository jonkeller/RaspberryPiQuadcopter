from IMU import IMU

class Drone:
    done = False
    imu = None

    def __init__(self):
        imu = IMU()

    def mainLoop(self):
        while not self.done:
            self.sense()
            self.move()

    def sense(self):
        imu.read()

    def move(self):
        print "Move"


