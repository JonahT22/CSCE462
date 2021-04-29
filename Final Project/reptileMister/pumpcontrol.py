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
# Relay disable variables
# Use these to check whether relay can be switched on
levelSwitchValue = True         # If False, water level too low
manualOverrideButton = False    # If True, button has been pressed once    

def setup():
    global outPin
    global pushBtn
    GPIO.setmode(GPIO.BCM)
    outPin = 22
    pushBtn = 19
    levelSwitch = 5
    GPIO.setup(outPin, GPIO.OUT, initial = 0)
    GPIO.setup(pushBtn, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(levelSwitch, GPIO.IN, GPIO.PUD_DOWN)
    # Add event callback to manually control the pump operation with a button (for testing)
    GPIO.add_event_detect(pushBtn, GPIO.RISING, callback=manualOverride)
    GPIO.add_event_detect(levelSwitch, GPIO.BOTH, callback=lambda x: levelSwitchChange(levelSwitch))

def manualOverride(channel):
    global manualOverrideButton
    if not manualOverrideButton:
        manualOverrideButton = True
        print("Manual Override activated - press button again to deactivate")
    else:
        manualOverrideButton = False
        print("Manual Override deactivated - press button again to activate")

# Keep track of levelSwitch state.
# Used as a check by the relay before turning on.
# Input: N/A
# Output: N/A
def levelSwitchChange(levelSwitch):
    global levelSwitchValue
    if(GPIO.input(levelSwitch) == 1):
        # Enable relay
        levelSwitchValue = True
        print("Water level OK")
    else:
        # Disable relay
        levelSwitchValue = False
        print("Water level low, needs attention!")

        
# Turns relay on so water pump can spray water into the tank.
# Can only do so if the manual override button hasn't been pressed
# and if the level switch
# Inputs: int seconds (to allow user to control spray length)
# Outputs: none
def runMister(seconds):
    try:
        if levelSwitchValue == True and manualOverrideButton == False:
            print("Turning relay on for {0} seconds".format(seconds))
            GPIO.output(outPin, GPIO.HIGH)
            time.sleep(seconds)
            GPIO.output(outPin, GPIO.LOW)
            print("Turning relay off")
        elif levelSwitchValue == False and manualOverrideButton == False:
            print("Can't switch on relay due to levelSwitch")
        elif levelSwitchValue == True and manualOverrideButton == True:
            print("Cant switch on relay due to button being pressed")
        else:
            # levelSwitch Value == False and manualOverrideButton == True
            print("Can't switch on relay due to both button and relay values")
            
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
