import RPi.GPIO as GPIO
import time


print(GPIO.RPI_INFO)

#Set GPIO pin mode
GPIO.setmode(GPIO.BOARD)

#Setting up output pin*******************************************************
#General format: GPIO.setup(pin_name, GPIO.OUT, initial_state (0 or 1))
#output1 = 8
#GPIO.setup(output1, GPIO.OUT, initial = 0)

#General format: GPIO.output(pin, state)
#GPIO.output(output1, 1)

"""
#simple blink function
output1 = 8
GPIO.setup(output1, GPIO.OUT, initial = 0)
try:
    while(True):
        #turn on, set as HIGH for 1 sec
        GPIO.output(output1, GPIO.HIGH)
        print("ON")
        time.sleep(1)
        #turn off, set as LOW for 1 sec
        GPIO.output(output1, GPIO.LOW)
        print("OFF")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")
"""    

"""
simple input testing function

input1 = 7
GPIO.setup(input1, GPIO.IN, GPIO.PUD_UP)
try:
    while(True):
        #print out input gathered
        print(GPIO.input(input1))
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")
"""

"""
simple state detection function
"""
#"""
input1 = 7
output1 = 8
GPIO.setup(input1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(output1, GPIO.OUT, initial = 0)
try:
    while(True):
        #Check input on pin 7
        if GPIO.input(input1) == 0:
            GPIO.output(output1, GPIO.HIGH)
            print("LED now on...")
        else:
            GPIO.output(output1, GPIO.LOW)
            print("LED now off...")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")

#"""
