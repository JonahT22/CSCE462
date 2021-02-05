import RPi.GPIO as GPIO
import time
import math
import sin_wave

#declare methods for generating each function
#move each of these to their own file

#Set up board
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#Set up output pin - which will send digital function's signal
#to the DAC chip.
function_signal = 37
GPIO.setup(function_signal, GPIO.OUT, initial = 0)

#Set up button_state + button_state change func
button_state = False;
def press_button(channel):
    button_state = True

button = 35
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

#Check for button press; if so, change button_state value.
GPIO.add_event_detect(button, GPIO.RISING, press_button, 600)

try:
    #1. Wait for button to be pressed"""
    while(not button_state):
        time.sleep(1)
        print(GPIO.input(button))
        print(button_state)
        if(button_state):
            print("Button triggered")    
            #2. Ask user for: function name (sq, tr, sin), frequency, 
            #max voltage (3 < x < 5V). Have three separate 
            #prompts for each input field.
            function_name = input("Enter desired function (sq, tr, sin):")
            function_name = function_name.capitalize()
            #3. Implement appropriate function
            if function_name == "SQ":
                #Call square wave func
                print("SQ func given")
            elif function_name == "TR":
                #Call tri wave func
                print("TR func given")
            elif function_name == "SIN":
                #Call sin wave func
                print("Sin func given")
            else:
                print("Try typing your function again")
        button_state = False
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Cleaning up...")
