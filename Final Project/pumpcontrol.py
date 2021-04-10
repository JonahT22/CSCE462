# This file handles controlling the relay module
# Wiring setup:
#    



import RPi.GPIO as GPIO
import time


print(GPIO.RPI_INFO)

#Set GPIO pin mode
GPIO.setmode(GPIO.BOARD)

btn = 40
output1 = 36
GPIO.setup(btn, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(output1, GPIO.OUT, initial = 0)

try:
	while(True):
		if(GPIO.input(btn) == 1):
			print("button on")
			GPIO.output(output1, GPIO.HIGH)
		else:
			print("off")
			GPIO.output(output1, GPIO.LOW)
		time.sleep(0.1)
except KeyboardInterrupt:
	GPIO.cleanup()
