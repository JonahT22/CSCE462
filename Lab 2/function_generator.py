import RPi.GPIO as GPIO
import time
import math
import sin_wave

#declare methods for generating each function
#move each of these to their own file
def square_wave():

def triangle_wave():

#Set up board
GPIO.setmode(GPIO.board)

#Set up output pin - which will send digital function's signal
#to the DAC chip.
function_signal = 37
GPIO.setup(function_signal, GPIO.OUT, initial = 0)


#1. Wait for push button input to start program


#2. Ask user for: function name (sq, tr, sin), frequency, max voltage (3 < x < 5V)
# have three separate prompts for each input field


#3. Parse input from user, generate correct function until next button input

