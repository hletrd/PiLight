# <del>P*Light</del> PiLight
* Clone of Yeelight based on Raspberry Pi
* Adjustable color temperatures
* Adjustable RGB value
* Uses GPIO port to control LEDs
 * You may use MOSFETs, or your own driver to drive your RGB LED.

## Running
* Run following
```
$ make
$ sudo python run.py
```
* Must give superuser permission.

## Running on startup
* Add following to /etc/crontab (If the program is in /home/pi/PiLight)
```
@reboot root cd /home/pi/PiLight && python run.py &
```
