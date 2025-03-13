from geoFence import *  
from reminders import * 
from led import *
from gps import *
import RPi.GPIO as GPIO


'''
DOCS FOR LATER ME

    TRASH REMINDER LED IS ON PINS [17,27,22]
    STATUS LED OF CODE IS ON PINS [10,9,11]

    GPS PINS ARE ON TX AND RX PINS ON PI
        REMEMBER:
            GPS RX pin goes to Raspi TX pin
            GPS TX pin goes to Raspi RX pin
        You wont get data out of the gps module if it isnt set-up correctly!

    WHEN PUBLISHING TO GITHUB DONT FORGET TO REMOVE HOME CORDS!!!
'''

# Initialize Classes
GYGPSV1 = GPS()
takeOutTrash = Reminder()
ParkOtherSide = Reminder()
ParkOurSide = Reminder()



Led = LED([17,27,22], True)
statusLED = LED([10,9,11], True)
statusLED.setColor([255,0,0])
statusLED.turnOn()

homeCoords = [0, 0]
radius = 0.0065814394  # in miles

# Create reminder
takeOutTrash.setWeekday("saturday", "Take out trashcans")

# Create LED for STATUSES
Led.setColor([24,135,98])
Led.turnOff()

# SLEEP TO ALLOW TIME FOR BACKGROUND PROCESSES TO OPEN
time.sleep(1)

# Turn status LED to green once code is setup
statusLED.setColor([0,255,0])
statusLED.turnOn()
try:
    while True:
        currentCoords = [GYGPSV1.getLatitude(), GYGPSV1.getLongitude()]
        if(currentCoords[0] == -1 or currentCoords[1] == -1):
            # Changed status LED to Yellow indicating GPS unable to get data
            statusLED.setColor([255,255,0])
            statusLED.turnOn()
            time.sleep(0.25)
            statusLED.turnOff()
            continue

        # Turn Status LED to Green
        statusLED.setColor([0,255,0])
        statusLED.turnOn()

        # Check if raspi is within 'home' cordinates
        raspi = geoFence(currentCoords, radius)
        reminderStatus, comment = takeOutTrash.getStatus() # comment is unused here, maybe later id want to add screen which is where it would become useful
        if(not ( raspi.is_inside(homeCoords) and reminderStatus)):
            Led.turnOff()
            continue


        #Run any code under this comment to run if raspi is within 'home'
        Led.turnOn()
        time.sleep(2)
except Exception as e:
    f = open('logs.txt', "a")
    f.write(e)
    f.close()
    GPIO.cleanup()

