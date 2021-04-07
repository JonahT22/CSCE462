import RPi.GPIO as GPIO
import Adafruit_DHT
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter

DHT_SENSOR = Adafruit_DHT.AM2302
GPIO.setmode(GPIO.BCM)
DHT_PIN = 18

startTime = perf_counter()
timevals = []
humidityvals = []

try:
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

		if humidity is not None and temperature is not None:
			print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
			timevals.append(perf_counter() - startTime)
			humidityvals.append(humidity)
		else:
			print("Failed to retrieve data from humidity sensor")

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Showing output")
	
plt.xlabel('Time')
plt.ylabel('Humidity')
plt.plot(timevals, humidityvals)
plt.show()
