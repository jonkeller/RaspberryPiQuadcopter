from IMU import IMU

class Drone:
    done = False
    imu = None

    def __init__(self):
        imu = IMU()
        # TODO: Light LEDs

    def mainLoop(self):
        while not self.done:
            self.sense()
            self.move()

    def sense(self):
        imu.read()
        # TODO: Sense from ultrasonics
        # TODO: Sense from GPS
        # TODO: Sense from LIDAR

    def move(self):
        print "Move"
        # TODO: use sensor data to decide where to move. Send appropriate commands to motors


