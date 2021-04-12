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
#		A-D side: resistor to 3.3V
#		B-C side: GPIO21, and pull-down resistor to GND

import RPi.GPIO as GPIO
import time

outPin = 0
pushBtn = 0

def setup():
    global outPin
    global pushBtn
    GPIO.setmode(GPIO.BOARD)
    outPin = 38
    pushBtn = 40
    GPIO.setup(outPin, GPIO.OUT, initial = 0)
    GPIO.setup(pushBtn, GPIO.IN, GPIO.PUD_DOWN)
    # Add event callback to manually control the pump operation with a button (for testing)
    GPIO.add_event_detect(pushBtn, GPIO.BOTH, callback=manualOverride)

def setOutputPin(pinNum):
    global outPin
    outPin = pinNum


def turnOn():
    GPIO.output(outPin, GPIO.HIGH)


def turnOff():
    GPIO.output(outPin, GPIO.LOW)


def manualOverride(channel):
    if(GPIO.input(pushBtn) == 1):
        GPIO.output(outPin, GPIO.HIGH)
    else:
        GPIO.output(outPin, GPIO.LOW)


# infinite loop, just in case this file is run on its own
setup()
try:
    setup()
    while(True):
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
