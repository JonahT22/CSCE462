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


def lightCycle():
    print("run light cycle")


# MAIN
try:
    # # Testing the 7-segment display
    # for i in range(9, -1, -1):
    #     segDisplay.setDisplayNum(panelPorts, i)
    #     time.sleep(0.1)
    # segDisplay.setDisplayNum(panelPorts, -1)  # clear the display
    usePolling = True  # use polling by default
    if(len(sys.argv) == 2):
        if(sys.arv[1] == "interrupt"):
            usePolling = False

    while(True):
        if(usePolling == True):
            if(GPIO.input(tl1_Button) == GPIO.HIGH):
                lightCycle()

    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")
