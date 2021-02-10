#import relevant libraries
import RPi.GPIO as GPIO
import time
import os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#set up board + ADC chip



#General structure of program:

#1. Find frequency (how?)

#2. Find max/min voltages (how?)

#3. Using previous two, use expected function values at specific intervals to determine
# type of function.

#4. Continuously check for frequency, make sure it's on the same function
