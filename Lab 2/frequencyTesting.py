import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
ledNum = 40
GPIO.setup(ledNum, GPIO.OUT)
GPIO.setwarnings(False)
tStep = 0.1  #starting frequency: 10 Hz
try:
    while 1:
        newfreq = input("please enter a new frequency: ")
        tStep = 1 / float(newfreq)
        t = 0
        while(t < 5):
            GPIO.output(ledNum, GPIO.HIGH)
            time.sleep(tStep)
            GPIO.output(ledNum, GPIO.LOW)
            time.sleep(tStep)
            t += tStep
        
except KeyboardInterrupt:
    GPIO.cleanup()

# Note for the future: to get an orange color, set frequency to 100, duty
# cycle to 90, send that signal to red, give orange full power
