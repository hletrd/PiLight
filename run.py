#try:
	#import RPi.GPIO as GPIO
#except:
	#print('No module named RPI found')
from flask import Flask, render_template, send_from_directory
#from htmlmin.minify import html_minify
import math
#import threading
#from time import sleep
from subprocess import Popen, PIPE, STDOUT

app = Flask(__name__)
tNow = 6600
rNow = 100
gNow = 100
bNow = 100

tMax = 12000
tmin = 1500

#PWMfreq = 100
rMax = 35
gMax = 48
bMax = 48

def colorTemptoRGB(colortemp):
	colortemp /= 100
	if colortemp <= 66:
		r = 255
		g = colortemp
		g = 99.4708025861 * math.log(g) - 161.1195681661
		if g < 0:
			g = 0
		if g > 255:
			g = 255
		if colortemp <= 19:
			b = 0
		elif colortemp == 66:
			b = 255
		else:
			b = colortemp - 10
			b = 138.5177312231 * math.log(b) - 305.0447927307
			if b < 0:
				b = 0
			if b > 255:
				b = 255
	else:
		r = colortemp - 60
		r = 329.698727446 * math.pow(r, -0.1332047592)
		g = colortemp - 60;
		g = 288.1221695283 * math.pow(g, -0.0755148492)
		if r < 0:
			r = 0
		if r > 255:
			r = 255
		if g < 0:
			g = 0
		if g > 255:
			g = 255
		b = 255
	return {'r': r, 'g': g, 'b': b}

def calcR(rawR):
	return int(rawR / 255.0 * rMax / 100 * colorTemptoRGB(tNow)['r']/255*1000)

def calcG(rawG):
	return int(rawG / 255.0 * gMax / 100 * colorTemptoRGB(tNow)['g']/255*1000)

def calcB(rawB):
	return int(rawB / 255.0 * bMax / 100 * colorTemptoRGB(tNow)['b']/255*1000)

"""class PWM(threading.Thread):
	def __init__(self, dc, color):
		threading.Thread.__init__(self)
		self.dc = dc
		self.color = color
		self.flag = True

	def run(self):
		if self.color == 'R':
			pin = rPin
		elif self.color == 'G':
			pin = gPin
		elif self.color == 'B':
			pin = bPin
		self.on = self.dc/10000
		self.off = (100-self.dc) / 10000
		while self.flag:
			GPIO.output(pin, 1)
			sleep(0.001)
			GPIO.output(pin, 0)
			sleep(0.01)"""

p = Popen(['./pwm'], stdout=PIPE, stdin=PIPE, stderr=PIPE)

try:
	#GPIO.setmode(GPIO.BOARD)
	#GPIO.setwarnings(False)
	#GPIO.setup(rPin, GPIO.OUT)
	#GPIO.setup(gPin, GPIO.OUT)
	#GPIO.setup(bPin, GPIO.OUT)
	#rLED = GPIO.PWM(rPin, PWMfreq)
	#gLED = GPIO.PWM(gPin, PWMfreq)
	#bLED = GPIO.PWM(bPin, PWMfreq)
	#rLED.start(calcR(rNow))
	#gLED.start(calcG(gNow))
	#bLED.start(calcB(bNow))
	#RPi.GPIO's PWM SUCKS!
	#tr = PWM(calcR(rNow), 'R')
	#tg = PWM(calcG(gNow), 'G')
	#tb = PWM(calcB(bNow), 'B')
	#tr.start()
	#tg.start()
	#tb.start()
	p.stdin.write(str(calcR(rNow)) + ' ' + str(calcG(gNow)) + ' ' + str(calcB(bNow)) + "\n")
	print str(calcR(rNow)) + ' ' + str(calcG(gNow)) + ' ' + str(calcB(bNow))
except:
	pass

@app.route('/')
def index():
	return render_template('_basic.html', tNow=tNow, rNow=rNow, gNow=gNow, bNow=bNow)

@app.route('/send/<int:t>/<int:r>/<int:g>/<int:b>')
def handlepost(t, r, g, b):
	global tNow, rNow, gNow, bNow, rLED, gLED, bLED, tMax, tmin
	if t > tMax:
		t = tMax
	elif t < tmin:
		t = tmin
	if r > 255:
		r = 255
	elif r < 0:
		r = 0
	if g > 255:
		g = 255
	elif g < 0:
		g = 0
	if b > 255:
		b = 255
	elif b < 0:
		b = 0
	tNow = t
	rNow = r
	gNow = g
	bNow = b
	#tr.flag = False
	#tg.flag = False
	#tb.flag = False
	#tr = PWM(calcR(rNow), 'R')
	#tg = PWM(calcG(gNow), 'G')
	#tb = PWM(calcB(bNow), 'B')
	#tr.start()
	#tg.start()
	#tb.start()
	p.stdin.write(str(calcR(rNow)) + ' ' + str(calcG(gNow)) + ' ' + str(calcB(bNow)) + "\n")
	print str(calcR(rNow)) + ' ' + str(calcG(gNow)) + ' ' + str(calcB(bNow))
	return 'succeed'

@app.route('/static/<path:path>')
def send_static(path):
	return send_from_directory(app.config['UPLOAD_FOLDER'], path, as_attachment=False)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)