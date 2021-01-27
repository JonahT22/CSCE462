import RPi.GPIO as GPIO
import time
import segDisplay

# NOTES:
# -To get an orangeish-yellow color, set frequency to 100, duty cycle to 90,
#  send that signal to the red terminal, give green full power

# OUTPUT PORTS
tl1_Red = 2
tl1_Yellow_R = 3  # The red terminal of the yellow light
tl1_Yellow_G = 4  # The green terminal of the yellow light
tl1_Green = 17
tl2_Red = 27
tl2_Yellow_R = 22 # The red terminal of the yellow light
tl2_Yellow_G = 10 # The green terminal of the yellow light
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
GPIO.setup(tl1_Yellow_R, GPIO.OUT, initial = 0)
GPIO.setup(tl1_Yellow_G, GPIO.OUT, initial = 0)
GPIO.setup(tl1_Green, GPIO.OUT, initial = 0)
GPIO.setup(tl2_Red, GPIO.OUT, initial = 0)
GPIO.setup(tl2_Yellow_R, GPIO.OUT, initial = 0)
GPIO.setup(tl2_Yellow_G, GPIO.OUT, initial = 0)
GPIO.setup(tl2_Green, GPIO.OUT, initial = 0)

for i in range(0, 7):
    GPIO.setup(panelPorts[i], GPIO.OUT, initial = 0)

# Create pwm outputs with default frequency of 100
tl1_R_pwm = GPIO.PWM(tl1_Yellow_R, 100)
tl2_R_pwm = GPIO.PWM(tl2_Yellow_R, 100)


# MAIN
try:
    # Testing the 7-segment display
    for i in range(9, -1, -1):
        segDisplay.setDisplayNum(panelPorts, i)
        time.sleep(1)
    segDisplay.setDisplayNum(panelPorts, -1)  # clear the display

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting...")



