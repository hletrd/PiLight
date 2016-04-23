try:
	import RPi.GPIO as GPIO
except:
	print('No module named RPI found')
from flask import Flask, render_template, send_from_directory
#from htmlmin.minify import html_minify
import math

app = Flask(__name__)
tNow = 6600
rNow = 255
gNow = 255
bNow = 255

tMax = 12000
tmin = 1500

PWMfreq = 1000
rMax = 50
gMax = 72
bMax = 72

rPin = 36
gPin = 38
bPin = 40

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
	return rawR / 255.0 * rMax / 100 * colorTemptoRGB(tNow)['r']/255*100

def calcG(rawG):
	return rawG / 255.0 * gMax / 100 * colorTemptoRGB(tNow)['g']/255*100

def calcB(rawB):
	return rawB / 255.0 * bMax / 100 * colorTemptoRGB(tNow)['b']/255*100

try:
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(rPin, GPIO.OUT)
	GPIO.setup(gPin, GPIO.OUT)
	GPIO.setup(bPin, GPIO.OUT)
	rLED = GPIO.PWM(rPin, PWMfreq)
	gLED = GPIO.PWM(gPin, PWMfreq)
	bLED = GPIO.PWM(bPin, PWMfreq)
	rLED.start(calcR(rNow))
	gLED.start(calcG(gNow))
	bLED.start(calcB(bNow))
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
	rLED.ChangeDutyCycle(calcR(rNow))
	gLED.ChangeDutyCycle(calcG(gNow))
	bLED.ChangeDutyCycle(calcB(bNow))
	return 'succeed'

@app.route('/static/<path:path>')
def send_static(path):
	return send_from_directory(app.config['UPLOAD_FOLDER'], path, as_attachment=False)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)