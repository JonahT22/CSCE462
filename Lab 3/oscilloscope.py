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
#num_samples = 0  # used for oscilloscope frequency measurement

def collectData():
    #global num_samples  # used for oscilloscope frequency measurement
    sum = 0
    for i in range(0, 2):
        sum += input_chan.voltage
    output = sum / 2.0
    #num_samples += 1  # used for oscilloscope frequency measurement
    return output

#Period finding function
#can change the zero requirement to just any arbitrary voltage value,
#in case not all functions are centered at zero.
def find_period():
    while collectData() > desired_voltage:
        pass
    while collectData() < desired_voltage:
        pass
    time_begin = time.time()        #first zero reached 

    #Loop until next zero voltage value found
    while collectData() > desired_voltage:
        pass
    while collectData() < desired_voltage:
        pass
    time_end = time.time()          #second zero reached
    period = time_end - time_begin
    return period
    
try:
    #startTime = time.perf_counter()  # used for oscillosope frequency measurement
    while(True):
        #1. Find frequency (how? - check for first instance of zero, sleep for a time)
        period = find_period()
        #sample a data point 1/8 of the way through the cycle
        sleeptime = abs(.125 * period - 0.00225)
        time.sleep(sleeptime)
        sample_average = collectData() # input_chan.voltage
        
        #2. Set the max and min voltage values
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
        
        #print("Sampling Frequency = ", num_samples / (time.perf_counter() - startTime))  # used for oscillosope frequency measurement
        print("Frequency = ", 1 / period)

except KeyboardInterrupt:
    print("Exiting...")

