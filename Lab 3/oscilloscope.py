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
desired_voltage = 1
sample_average = 0.0
error_threshold = 0.1

def collectData():
    sum = 0
    for i in range(0, 2):
        sum += input_chan.voltage
    output = sum / 2.0
    return output

#Period finding function
#can change the zero requirement to just any arbitrary voltage value,
#in case not all functions are centered at zero.
def find_period():
    """while input_chan.voltage > desired_voltage:
        pass
    while input_chan.voltage < desired_voltage:
        pass                        #do nothing; wait until zero voltage is measured
    """
    while collectData() > desired_voltage:
        pass
    while collectData() < desired_voltage:
        pass
    #print("voltage = ", input_chan.voltage)
    time_begin = time.time()        #first zero reached 
    #print(time_begin)
    #time.sleep(0.02)                #eliminate jitter by sleeping
    #Loop until next zero voltage value found
    """
    while input_chan.voltage > desired_voltage:
        pass                        #do nothing
    #time.sleep(0.02)
    while input_chan.voltage < desired_voltage:
        pass
    """
    while collectData() > desired_voltage:
        pass
    while collectData() < desired_voltage:
        pass
    #time.sleep(0.02)
    #print("voltage = ", input_chan.voltage)
    time_end = time.time()          #second zero reached
    #print(time_end)
    #print("Diff = ", time_end - time_begin)
    period = time_end - time_begin
    #freq = 1.0 / ( (time_end - time_begin))
    return period

#Max/min voltage finding function
#def find_max_min(freq):
    
try:
    while(True):
        #1. Find frequency (how? - check for first instance of zero, sleep for a time)
        # The time.sleep() works for eliminating jitter since there is a narrow band of possible
        # frequencies (1 - 20 Hz).
        period = find_period()
        sleeptime = abs(.125 * period - 0.00225)
        time.sleep(sleeptime)
        #sample 10 data pointa
        sample_average = input_chan.voltage
        """
        for i in range(0,2):
            sample_average += input_chan.voltage
        sample_average /= 2.0"""
        #print("Frequency: ", 1.0 / period)
        #print("Average sampled data: ", sample_average)

        #2. Find max/min voltages (how?)
        min_volt = 0
        max_volt = 2

        #3. Using previous two, use expected function values at specific intervals to determine
        # type of function.
        # specific interval = 1/8 * period
        # assumption: function is rising to its max value when we make the check. 
        expected_amplitude_sin =  (max_volt - min_volt) * 0.707 / 2 + (max_volt + min_volt) / 2
        expected_amplitude_square = max_volt
        expected_amplitude_tri = .75 * (max_volt - min_volt) + min_volt

        #Compare sample sum to expected values
        if abs(expected_amplitude_sin - sample_average) < error_threshold:
            #Sin wave likely found
            print("Sin,   ", end='')
        elif abs(expected_amplitude_tri - sample_average) < error_threshold:
            #Tri wave likely found
            print("Tri,   ", end='')
        elif abs(expected_amplitude_square - sample_average) < error_threshold:
            #Square wave likely found
            print("Square ", end='')
        else:
            print("bruh   ", end='')
        
        print("Frequency = ", 1 / period)

except KeyboardInterrupt:
    print("Exiting...")

#4. Continuously check for frequency, make sure it's on the same function (tolerance = within 0.5 Hz of defined value)
