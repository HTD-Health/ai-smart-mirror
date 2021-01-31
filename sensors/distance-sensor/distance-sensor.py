#!/usr/bin/python


# Import required Python libraries
import time
import csv
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

print "Ultrasonic Measurement"
# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.3)



with open('distance.csv', mode='w') as csv_file:
    fieldnames = ['time', 'distance']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    i = 0
    try:
        while True:
            # Send 10us pulse to trigger
            GPIO.output(GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)
            start = time.time()
            stop = time.time()
            while GPIO.input(GPIO_ECHO)==0:
              start = time.time()
            while GPIO.input(GPIO_ECHO)==1:
              stop = time.time()

            # Calculate pulse length
            elapsed = stop-start

            # Distance pulse travelled in that time is time
            # multiplied by the speed of sound (cm/s)
            distancet = elapsed * 34300

            # That was the distance there and back so halve the value
            distance = round(distancet / 2, 2)

            print "Distance :", distance
            
            writer.writerow({'time': i, 'distance': distance})
            i+=1

            time.sleep(0.1)
    except KeyboardInterrupt:
        print "End by user keyboard interrupt"
    except:
        print "Unexpected Error"


# Reset GPIO settings
GPIO.cleanup()

