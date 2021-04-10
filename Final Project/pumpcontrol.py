# This file handles controlling the relay module
# For now, it simply controls a on/off switch, but later will also 
# check for float sensor and give output warnings
# 
# Wiring setup:
#	Relay Module:
#		IN: GPIO20
#		DC+: 3.3V
#		DC-: GND
#		NO: GND wire of device
#		COM: GND of power source (i.e. wall plug)
#		(Connect v+ of device straight to the power source. See https://www.electronicshub.org/control-a-relay-using-raspberry-pi/)
#	Push Button:
#		A-D side: 3.3V
#		B-C side: GPIO21, and pull-down resistor to GND

import RPi.GPIO as GPIO

#Set GPIO pin mode
GPIO.setmode(GPIO.BOARD)
outPin = 38
GPIO.setup(outPin, GPIO.OUT, initial = 0)


def setOutputPin(pinNum):
	outPin = pinNum


def turnOn():
	GPIO.output(outPin, GPIO.HIGH)


def turnOff():
	GPIO.output(outPin, GPIO.LOW)


# Add event callbacks to manually control the pump operation with a button (for testing)
pushBtn = 40
GPIO.setup(pushBtn, GPIO.IN, GPIO.PUD_DOWN)
GPIO.add_event_detect(btnPin, GPIO.RISING, callback=turnOn, bouncetime=600)
GPIO.add_event_detect(btnPin, GPIO.FALLING, callback=turnOff, bouncetime=600)