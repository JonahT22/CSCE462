import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
ledNum = 40
GPIO.setup(ledNum, GPIO.OUT)
# starting with frequency 100
pwm = GPIO.PWM(ledNum, 100)
# stating with 0, that is off state
pwm.start(0)
try:
    while 1:
        # duty cycle from 0% to 100%
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
        # duty cycle from 100% to 0%
        for dc in range(100, -1, -5):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()

# Note for the future: to get an orange color, set frequency to 100, duty
# cycle to 90, send that signal to red, give orange full power

