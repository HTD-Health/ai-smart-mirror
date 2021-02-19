#!/usr/bin/python
# Import required Python libraries
import time

import RPi.GPIO as GPIO

# Define GPIO to use on Pi
# @TODO: move pin consts to config file
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# @TODO: move these consts to config file
TRIGGER_PULSE_TIME = 0.00001  # Needs to be 10us pulse to trigger the sensor
SLEEP_TIME = 0.1
SENSOR_SETTLE_TIME = 0.3
TIME_PRECISION = 0.0001  # s - to low value creates problems with spotting objects close to the sensor

SPEED_OF_SOUND = 34300  # cm/s
HALF_SPEED_OF_SOUND = SPEED_OF_SOUND / 2


def send_trigger():
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(TRIGGER_PULSE_TIME)
    GPIO.output(GPIO_TRIGGER, False)


# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)  # Echo

print("Ultrasonic Measurement")
# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(SENSOR_SETTLE_TIME)


try:
    while True:
        send_trigger()

        while GPIO.input(GPIO_ECHO) == 0:
            time.sleep(TIME_PRECISION)
        echo_start = time.time()

        while GPIO.input(GPIO_ECHO) == 1:
            time.sleep(TIME_PRECISION)
        echo_stop = time.time()

        # Calculate pulse length
        pulse_duration = echo_stop - echo_start
        distance = round(pulse_duration * HALF_SPEED_OF_SOUND, 2)

        print(f"Ultrasonic Measurement - Distance: {distance} cm")

        time.sleep(SLEEP_TIME)
except KeyboardInterrupt:
    print("End by user keyboard interrupt")
finally:
    GPIO.cleanup()

# Reset GPIO settings
GPIO.cleanup()
