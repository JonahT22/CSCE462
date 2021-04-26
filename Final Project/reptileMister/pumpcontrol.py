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
    GPIO.setmode(GPIO.BCM)
    outPin = 22
    pushBtn = 19
    GPIO.setup(outPin, GPIO.OUT, initial = 0)
    GPIO.setup(pushBtn, GPIO.IN, GPIO.PUD_DOWN)
    # Add event callback to manually control the pump operation with a button (for testing)
    GPIO.add_event_detect(pushBtn, GPIO.BOTH, callback=manualOverride)

def manualOverride(channel):
    if(GPIO.input(pushBtn) == 1):
        GPIO.output(outPin, GPIO.HIGH)
        print("Button pushed")
    else:
        GPIO.output(outPin, GPIO.LOW)

# Turns relay on so water pump can spray water into the tank.
# Inputs: int seconds (to allow user to control spray length)
# Outputs: none
def runMister(seconds):
    print("Turning relay on for {0} seconds".format(seconds))
    try:
        GPIO.output(outPin, GPIO.HIGH)
        time.sleep(seconds)
        GPIO.output(outPin, GPIO.LOW)
        print("Turning relay off")
    except KeyboardInterrupt:
        GPIO.cleanup()

# infinite loop, just in case this file is run on its own
# setup()
#try:
#    setup()
#    while(True):
#        time.sleep(0.1)
#except KeyboardInterrupt:
#    GPIO.cleanup()
