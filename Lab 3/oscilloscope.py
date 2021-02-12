#import relevant libraries
#import RPi.GPIO as GPIO
import time
import os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import math

#set up board + ADC chip
#create spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

#create the chip select (which port slave chip is connected to)
cs = digitalio.DigitalInOut(board.D22)

#create MCP object
mcp = MCP.MCP3008(spi, cs)

#create an analog input channel on pin 0 of ADC
input_chan = AnalogIn(mcp, MCP.P0)

#General structure of program:
freq = 0.0
freq_change = False
desired_voltage = 1

#Frequency finding function
#can change the zero requirement to just any arbitrary voltage value,
#in case not all functions are centered at zero.
def find_frequency():
    while input_chan.voltage > desired_voltage:
        pass
    while input_chan.voltage < desired_voltage:
        pass                        #do nothing; wait until zero voltage is measured
    print("voltage = ", input_chan.voltage)
    time_begin = time.time()        #first zero reached 
    print(time_begin)
    #time.sleep(0.04)                #eliminate jitter by sleeping
    #Loop until next zero voltage value found
    while input_chan.voltage > desired_voltage:
        pass                        #do nothing
    while input_chan.voltage < desired_voltage:
        pass
    print("voltage = ", input_chan.voltage)
    time_end = time.time()          #second zero reached
    print(time_end)
    print("Diff = ", time_end - time_begin)
    freq = 1.0 / ( (time_end - time_begin))
    return freq

#Max/min voltage finding function
#def find_max_min(freq):
    
try:
#1. Find frequency (how? - check for first instance of zero, sleep for a time)
# The time.sleep() works for eliminating jitter since there is a narrow band of possible
# frequencies (1 - 20 Hz).
    freq = find_frequency()
    print(freq)

#2. Find max/min voltages (how?)
    min_volt = 0
    max_volt = 2

#3. Using previous two, use expected function values at specific intervals to determine
# type of function.

except KeyboardInterrupt:
    print("Exiting...")

#4. Continuously check for frequency, make sure it's on the same function (tolerance = within 0.5 Hz of defined value)
