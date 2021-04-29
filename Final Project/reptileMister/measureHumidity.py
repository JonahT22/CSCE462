import RPi.GPIO as GPIO
import Adafruit_DHT
import numpy as np
import matplotlib.pyplot as plt
import time
from time import perf_counter
import pumpcontrol as pcntrl
import sendEmail as email

# DHT_SENSOR = Adafruit_DHT.AM2302
print("Setting up humidity sensor")
DHT_SENSOR = Adafruit_DHT.DHT22
GPIO.setmode(GPIO.BCM)
DHT_PIN = 24
emailContent = "Time = Humidity value<br>"

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
def avgHumidity(humidityvals, humidityvalsMaxSize, currentTime):
    avgHumidity = 0.0
    for h in humidityvals:
        avgHumidity += h
    avgHumidity /= humidityvalsMaxSize
    global emailContent 
    emailContent = emailContent + currentTime + "= " + str(avgHumidity) + "<br>"
    return avgHumidity

def sendEmail(sendTo, emailSubject, message):
    # Send email
    sender = email.Emailer()
    sender.sendmail(sendTo, emailSubject, message)
    print("Email with humidity data sent!")

    # Reset string of data for next day
    global emailContent 
    emailContent = "Time = Humidity value\n"


#Set up relay and pi connections
pcntrl.setup()
mistingTime = 2
TESTING = True      # ONLY TRUE IF PROGRAM IS BEING TESTED!!

# Turn on relay at specific times of day (within 1 minute tolerance)
# Immediately after, gather humidity data.
print("Starting program")
try:
    # Keep track of whether humidity and misting has happened within the minute
    humidityMeasured = False
    misted = False
    
    while(True):
        # Gather time
        # Time is in military format
        t = time.localtime()
        currentTime = time.strftime("%H:%M", t)
        # print("Current time: {0}".format(currentTime))
        mistTime1, mistTime2 = "08:00", "16:00"
        # Measure humidity if it has not been done already
        if humidityMeasured == False:
            if currentTime[3:] == "00" or TESTING == True:
                # Display current time
                print("Current time: {0}".format(currentTime))

                # Measure humidity data and display graph
                humidityvalsMaxSize = 5
                humidityvals = measureHumidity(humidityvalsMaxSize)

                #Find average humidity of points
                humidityAverage = avgHumidity(humidityvals, humidityvalsMaxSize, currentTime)
                
                # Make sure humidity isn't measured again until designated time:
                humidityMeasured = True
        else:
            # Reset humidityMeasured after a minute has passed
            # Allows humidity checks to occur at specific times only
            
            # Check if the time ends in "01"
            if currentTime[3:] == "01" or TESTING == True:
                humidityMeasured = False
                print("humidityMeasured value reset")

        if misted == False:
            if currentTime == mistTime1 or currentTime == mistTime2 or TESTING == True:
                # Run the relay to mist the tank1
                pcntrl.runMister(mistingTime)
                misted = True
        else:
            # Reset misted after a minute has passed
            # Allows misting to occur at specific times only
            if currentTime[3:] == "01" or TESTING == True:
                misted = False
                print("misted value reset")

        # Finally, send data in an email once per day
        if currentTime == "00:00" or TESTING == True:
            # send email
            sendTo = 'ostrich.bagelwocreamcheese@gmail.com'
            emailSubject = "Hello World"
            sendEmail(sendTo, emailSubject, emailContent)

        # Don't continuously waste power on a polling loop
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()



