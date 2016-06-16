# <del>P*Light</del> PiLight
* Clone of Yeelight based on Raspberry Pi
* Adjustable color temperatures
* Adjustable RGB value
* Uses GPIO port to control LEDs
 * You may use MOSFETs, or your own driver to drive your RGB LED.

## Hardware
* Connect 3 outputs from GPIO 16, GPIO 20, GPIO 21.
* Connect each gpio channel with RGB LED as following circuit
![circuit](https://github.com/hletrd/PiLight/blob/master/circuit.jpg)
 * Sorry for bad drawing, but now I don't have any tool to draw schematics.
 * I used a LED part from [adafruit](https://www.adafruit.com/product/2524).
  * I'd recommend you to use cooling fans, or large heatsink for LED.

## Setting up
* Install [pigpio](http://abyz.co.uk/rpi/pigpio/)
```
$ rm pigpio.zip
$ sudo rm -rf PIGPIO
$ wget abyz.co.uk/rpi/pigpio/pigpio.zip
$ unzip pigpio.zip
$ cd PIGPIO
$ make -j4
$ sudo make install
```
* clone PiLight
```
$ sudo apt-get install git
$ git clone https://github.com/hletrd/PiLight
```
* cd to PiLight directory, and compile pwm.c
```
$ make
```

## Running
* Run following
```
$ sudo python run.py
```
* Must give superuser permission.

## Running on startup
* Add following to /etc/crontab (If the program is in /home/pi/PiLight)
```
@reboot root cd /home/pi/PiLight && python run.py &
```
