import RPi.GPIO as GPIO
import time
import segDisplay
import sys

# OUTPUT PORTS
tl1_Red = 2
tl1_Blue = 3
tl1_Green = 17
tl2_Red = 27
tl2_Blue = 22
tl2_Green = 9

# an array holding the port numbers of each display segment
#     (order:  a, b, c,  d,  e,  f,  g)
panelPorts = [11, 5, 6, 13, 19, 26, 14]

# INPUT PORTS
tl1_Button = 15

# SETUP
GPIO.setwarnings(False)  # Stop GPIO from warning that we're using some
                         # multi-purpose pins as GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(tl1_Red, GPIO.OUT, initial = 0)
GPIO.setup(tl1_Blue, GPIO.OUT, initial = 0)
GPIO.setup(tl1_Green, GPIO.OUT, initial = 0)
GPIO.setup(tl2_Red, GPIO.OUT, initial = 0)
GPIO.setup(tl2_Blue, GPIO.OUT, initial = 0)
GPIO.setup(tl2_Green, GPIO.OUT, initial = 0)

for i in range(0, 7):
    GPIO.setup(panelPorts[i], GPIO.OUT, initial = 0)

GPIO.setup(tl1_Button, GPIO.IN, GPIO.PUD_DOWN)


def blink(lightPort):
    GPIO.output(lightPort, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(lightPort, GPIO.LOW)
    time.sleep(0.5)


def lightCycle(channel):
    # Note: lightCycle must take in 1 input arg, but it is not used
    # this input arg is automatically sent when it is called via an interrupt
    print("Detected button press...")
    GPIO.output(tl2_Green, GPIO.LOW)
    for i in range(0, 3):
        blink(tl2_Blue)
    GPIO.output(tl2_Red, GPIO.HIGH)

    GPIO.output(tl1_Red, GPIO.LOW)
    GPIO.output(tl1_Green, GPIO.HIGH)
    # begin the countdown
    for i in range(9, -1, -1):
        segDisplay.setDisplayNum(panelPorts, i)
        if i > 4:
            time.sleep(1)
        elif i > 0:
            GPIO.output(tl1_Green, GPIO.LOW)
            blink(tl1_Blue)
        else: 
            GPIO.output(tl1_Red, GPIO.HIGH)
            time.sleep(1)
    segDisplay.setDisplayNum(panelPorts, -1)  # clear the display
    GPIO.output(tl2_Red, GPIO.LOW)
    GPIO.output(tl2_Green, GPIO.HIGH)
    time.sleep(7)  # wait a bit longer so that the whole function takes 20 seconds


# MAIN
try:
    usePolling = True  # use polling by default
    if len(sys.argv) == 2:
        if sys.argv[1] == "interrupt":
            usePolling = False
            # Set the lightcycle function to run as a separate thread when button is pressed
            GPIO.add_event_detect(tl1_Button, GPIO.RISING, lightCycle, 600)

    GPIO.output(tl2_Green, GPIO.HIGH)
    GPIO.output(tl1_Red, GPIO.HIGH)
    canPress = True
    while True:
        if usePolling == True:
            if GPIO.input(tl1_Button) == GPIO.HIGH and canPress == True:
                canPress = False
                lightCycle(0)  # include the 20 second wait in this function
                canPress = True
        if usePolling == False:
            time.sleep(1)  # Do nothing, but don't hog the CPU i
    # TODO: add extra delays to the lightcycle function so that it takes 20s
    # TODO: add interrupt support via the "interrupt" input arg

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")
