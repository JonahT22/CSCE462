import RPi.GPIO as GPIO
import time
import math
import sin_wave

#declare methods for generating each function
def square_wave():

def triange_wave():

#Set up board
GPIO.setmode(GPIO.board)

#Set up output pin - which will send digital function's signal
#to the DAC chip.
function_signal = 37
GPIO.setup(function_signal, GPIO.OUT, initial = 0)


#1. Wait for push button input to start program


#2. Ask user for: function name (s, t, sin), frequency, max voltage (up to 5V?)


#3. Parse input from user, generate correct function until next button input

