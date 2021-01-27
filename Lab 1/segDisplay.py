import RPi.GPIO as GPIO


def b2GPIO(bVal):
    """Converts binary value to GPIO.HIGH or GPIO.LOW"""
    if(bVal == 0):
        return GPIO.LOW
    else:
        return GPIO.HIGH


def setDisplayNum(displayPorts, newNum):
    """Sets the GPIO output pins given in the displayPorts array
    so that the newNum is shown on the display"""
    if(displayPorts.len() != 7):
        print("ERROR: displayPorts must be a list of size 7")
        return False
    
    segList = []  # variable to hold binary values for each segment
                  # in the order: a, b, c, d, e, f, g
    # Check which number was inputted, set a list for the correct display values
    if(newNum == 0):
        segList = [1, 1, 1, 1, 1, 1, 0]
    elif(newNum == 1):
        segList = [0, 1, 1, 0, 0, 0, 0]
    elif(newNum == 2):
        segList = [1, 1, 0, 1, 1, 0, 1]
    elif(newNum == 3):
        segList = [1, 1, 1, 1, 0, 0, 1]
    elif(newNum == 4):
        segList = [0, 1, 1, 0, 0, 1, 1]
    elif(newNum == 5):
        segList = [1, 0, 1, 1, 0, 1, 1]
    else:
        print("haven't programmed ", newNum, " yet")

    # Set all of the display port values based on the binary data in segList
    for i in range(0, 7):
        GPIO.output(displayPorts[i], b2GPIO(segList[i]))
    
    # Finished successfully
    return True

