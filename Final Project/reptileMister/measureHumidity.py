import RPi.GPIO as GPIO
import Adafruit_DHT
import numpy as np
import matplotlib.pyplot as plt
import time
from time import perf_counter
import pumpcontrol as pcntrl

# DHT_SENSOR = Adafruit_DHT.AM2302
DHT_SENSOR = Adafruit_DHT.DHT22
GPIO.setmode(GPIO.BCM)
DHT_PIN = 24

def measureHumidity(humidityvalsMaxSize):
    startTime = perf_counter()
    timevals = []
    humidityvals = []

    try:
        while len(humidityvals) < humidityvalsMaxSize:
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
    return humidityvals

# Return average humidity value
def avgHumidity(humidityvals, humidityvalsMaxSize):
    avgHumidity = 0.0
    for h in humidityvals:
        avgHumidity += h
    avgHumidity /= humidityvalsMaxSize
    return avgHumidity

#Set up relay and pi connections
pcntrl.setup()
mistingTime = 2

try:
    while(True):
        t = time.localtime()
        currentTime = time.strftime("%H:%M", t)
        print("Current time: {0}".format(currentTime))
        mistTime1, mistTime2, testTime = "08:00", "16:00", "14:50"
        if currentTime == mistTime1 or currentTime == mistTime2 or currentTime == testTime:
            # Run the relay to mist the tank
            pcntrl.runMister(mistingTime)
        #Measure humidity data and keep
        humidityvalsMaxSize = 5
        humidityvals = measureHumidity(humidityvalsMaxSize)
        
        #Find average humidity of points
        humidityAverage = avgHumidity(humidityvals, humidityvalsMaxSize)
except KeyboardInterrupt:
    GPIO.cleanup()



