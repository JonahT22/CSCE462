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

#Check for button press; if so, change button_state value.
GPIO.add_event_detect(button, GPIO.BOTH, press_button, 600)

# resolution of the waveforms: smaller is more detailed but slower
tStep = 0.0005

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
                if function_name == "sq" or function_name == "tr" or function_name == "sin":
                    nameGood = True
                else:
                    print("    invalid function name! please try again")
            while not freqGood:
                frequency_string = raw_input("Enter desired frequency (up to 20 Hz): ")
                frequency = float(frequency_string)
                #if frequency <= 20 and frequency > 0:
                freqGood = True
                #else:
                #    print("    invalid frequency! please try again")
            while not voltGood:
                max_voltage_string = raw_input("Enter maximum output voltage (2.7 - 5.0 V): ")
                max_voltage = float(max_voltage_string)
                if max_voltage <= 5.0 and max_voltage >= 2.7:
                    voltGood = True
                else:
                    print("    invalid voltage! please try again")
            
            #3. Implement appropriate function
            button_state = False
            t = 0.0  # time since the waveform began
            if function_name == "sq":
                #Call square wave func
                print("Square function given")
                period = 1 / frequency
                dac_voltage = int((max_voltage / 5.0) * 4096)  #calculate value to set DAC to
                while not button_state:
                    rem = math.fmod(t, period) / period  # some value between 0 and 1
                    if rem > 0.5:
                        dac.set_voltage(dac_voltage)
                    else:
                        dac.set_voltage(0)
                    t += tStep
                    time.sleep(tStep)
            elif function_name == "tr":
                #Call tri wave func
                print("Triangle function given")
                period = 1 / (2 * frequency)
                while not button_state:
                    voltage = math.fabs((2 * math.fmod(t, period) / period) - 1) * (max_voltage / 5) * 4096
                    dac.set_voltage(int(voltage))
                    t += tStep
                    time.sleep(tStep)
            elif function_name == "sin":
                #Call sin wave func
                print("Sine function given")
                while not button_state:
                    voltage = (0.2 * max_voltage) * (.5 * (1.0 + math.sin(2*math.pi*frequency*t))) * 4096
                    dac.set_voltage(int(voltage))
                    t += tStep  # tStep is defined above main
                    time.sleep(tStep)
                    time.sleep(tStep)
            else:
                print("Incorrect function name given, press button to try again")
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Cleaning up...")
