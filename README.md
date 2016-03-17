# Raspberry Pi Quadcopter

In this project, I am building a quadcopter powered by a Raspberry Pi.

The hardware side of this project was started on February 1, 2016, and I seem to be going in cycles of about 2 weeks of working on hardware (thus no Github activity) and then 2 weeks of working on software.

## Quadcopter Parts List:
* [4x brushless motors and ESCs](https://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=76073) - [ESC User Manual](http://www.flyingtech.co.uk/sites/default/files/product_files/AfroESC%2020A%20USER%20MANUAL_0.pdf)
* [Battery](https://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=84097), [SBEC](https://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=64373), and [low-voltage alarm](https://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=58506). I would suggest getting a smaller battery than I did, so it will fit in the interior of the quad frame. Mine is huge so I had to mount it on top.
* [Raspberry Pi Model B](https://www.raspberrypi.org/products/model-b/). I originally tried to use a Pi 2, but the battery wouldn't supply enough power to keep it on.
* [Adafruit 16-Channel Servo Driver](https://www.adafruit.com/product/815)
* [GPS](https://www.adafruit.com/products/746)
* [10-DOF IMU](https://www.adafruit.com/products/1604)
* Maybe a [LIDAR-Lite](http://pulsedlight3d.com/) (link goes to v2 but mine is the now-discontinued v1)
* An [ultrasonic range sensors](http://www.robotshop.com/en/hc-sr04-ultrasonic-range-finder.html) - maybe up to 5 later
* [Pi camera](https://www.raspberrypi.org/products/camera-module/)
* Wifi USB adapter. It will act as an access point, allowing connection from another device which may be used to control the quadcopter.
* LEDs
* [Frame](https://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=66323) and [propellers](https://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=84400)
* A perfboard, since the connections are sturdier than those of a breadboard.

## Photos/Videos:

2/2/2016: Frame, motors, ESCs, propellers, and battery:

![Photo of drone](https://raw.githubusercontent.com/jonkeller/RaspberryPiQuadcopter/master/doc/img/IMG_20160202_175932.jpg)

2/27/2016: [Video of first...um..."flight"](https://www.youtube.com/watch?v=OnDQe11cgWQ)

