import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
ledNum = 40
GPIO.setup(ledNum, GPIO.OUT)
# starting with frequency 100
pwm = GPIO.PWM(ledNum, 1)
# stating with 0, that is off state
pwm.start(0)
try:
    while 1:
        newfreq = input("please enter a new frequency: ")
        pwm.ChangeFrequency(newfreq)
        time.sleep(.1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

# Note for the future: to get an orange color, set frequency to 100, duty
# cycle to 90, send that signal to red, give orange full power
