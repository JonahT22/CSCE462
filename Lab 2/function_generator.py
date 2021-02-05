import RPi.GPIO as GPIO
import Adafruit_MCP4725
import time
import math
import sin_wave

#Set up board/DAC
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
dac = Adafruit_MCP4725.MCP4725()
#Set up output pin - which will send digital function's signal
#to the DAC chip.
function_signal = 37
GPIO.setup(function_signal, GPIO.OUT, initial = 0)

#Set up button_state + button_state change func
button = 35
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

button_state = False
def press_button(channel):
    global button_state
    button_state = True
    #print("button state = ", button_state)

#Assuming frequencies and max voltage are not entered incorrectly
def square_wave(frequency, max_voltage):
    period = 1 / frequency      #total period of entire wave
    period = period / 2         #split period in half for length for each on/off cycle
    dac_voltage = max_voltage * 4096/5  #calculate value to set DAC to
    dac.set_voltage(dac_voltage)
    time.sleep(period)
    dac.set_voltage(0)
    time.sleep(period)


#Check for button press; if so, change button_state value.
GPIO.add_event_detect(button, GPIO.BOTH, press_button, 600)

try:
    #1. Wait for button to be pressed"""
    while(True):
        #print(GPIO.input(button))
        #print(button_state)
        if(button_state):
            print("Button triggered")  
            # Keep track of these variables for validating user input 
            nameGood = False
            freqGood = False
            voltGood = False 
            #2. Ask user for: function name (sq, tr, sin), frequency, 
            #max voltage (3 < x < 5V). Have three separate 
            #prompts for each input field.
            while not nameGood:
                function_name = raw_input("Enter desired function (sq, tr, sin): ")
                if function_name not in ("sq", "tr", "sin"):
                    nameGood = True
                else:
                    print("    invalid function name! please try again")
            while not freqGood:
                frequency_string = raw_input("Enter desired frequency (up to 20 Hz): ")
                frequency = float(frequency_string)
                if frequency <= 20 and frequency > 0:
                    freqGood = True
                else:
                    print("    invalid frequency! please try again")
            while not voltGood:
                max_voltage_string = raw_input("Enter maximum output voltage (2.7 - 5.0 V): ")
                max_voltage = float(max_voltage_string)
                if max_voltage <= 5.0 and max_voltage >= 2.7:
                    voltGood = True
                else:
                    print("    invalid voltage! please try again")
            
            #3. Implement appropriate function
            button_state = False
            if function_name == "sq":
                #Call square wave func
                #print("sq func given")
                while not button_state:
                    #square_wave(frequency, max_voltage)
                    print("sq wave func")
                    time.sleep(1)
            elif function_name == "tr":
                #Call tri wave func
                while not button_state:
                    print("tr func given")
                    time.sleep(1)
            elif function_name == "sin":
                #Call sin wave func
                while not button_state:
                    print("Sin func given")
                    time.sleep(1)
            else:
                print("Incorrect function name given, press button to try again")
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Cleaning up...")
