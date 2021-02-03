import time
import RPi.GPIO as GPIO
import math

# Import the MCP4725 module.
import Adafruit_MCP4725

# Create a DAC instance.
dac = Adafruit_MCP4725.MCP4725()

# Note you can change the I2C address from its default (0x62), and/or the I2C
# bus by passing in these optional parameters:
#dac = Adafruit_MCP4725.MCP4725(address=0x49, busnum=1)

# Loop forever alternating through different voltage outputs.
print('Press Ctrl-C to quit...')
try:
    t = 0.0
    tStep = 0.05
    while True:
        voltage = 2048 * (1.0 + .5 * math.sin(6.2832*t))
        dac.set_voltage(int(voltage))
        t += tStep
        time.sleep(0.0005)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")