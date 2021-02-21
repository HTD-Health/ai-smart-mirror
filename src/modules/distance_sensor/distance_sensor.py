#!/usr/bin/python
# Import required Python libraries
import time
import argparse
import sys

import RPi.GPIO as GPIO

# @TODO: move these consts to config file
SLEEP_TIME = 0.1
SENSOR_SETTLE_TIME = 0.3
TIME_PRECISION = 0.0001  # s - to low value creates problems with spotting objects close to the sensor

SPEED_OF_SOUND = 34300  # cm/s
HALF_SPEED_OF_SOUND = SPEED_OF_SOUND / 2
TRIGGER_PULSE_TIME = 0.00001  # Needs to be 10us pulse to trigger the sensor


def send_trigger(trigger_pin):
    # Send pulse to trigger
    GPIO.output(trigger_pin, True)
    time.sleep(TRIGGER_PULSE_TIME)
    GPIO.output(trigger_pin, False)


def handle_echo_pin_change(channel):
    # Check if the pin is in High or Low state
    if GPIO.input(channel):
        global echo_start
        echo_start = time.time()
    else:
        global echo_stop
        echo_stop = time.time()


def run_ultrasonic_sensor(trigger_pin, echo_pin):
    send_trigger(trigger_pin)

    # Calculate pulse length
    pulse_duration = echo_stop - echo_start
    calculated_distance = round(pulse_duration * HALF_SPEED_OF_SOUND, 2)

    return calculated_distance


def main():
    # @TODO: Decide how to pass Pins - via console arguments or Consts from the config file.
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser()

    # Argument 1: Trigger output pin
    parser.add_argument('--trig', type=int, default=16, help='PIN with TRIGGER output PIN.')
    # Argument 2: Echo input pin
    parser.add_argument('--echo', type=int, default=18, help='PIN with ECHO input PIN.')

    # Get command line arguments
    init_args = parser.parse_args()
    trigger_pin = init_args.trig
    echo_pin = init_args.echo

    print("Ultrasonic Measurement. Setting up GPIO...")

    # GPIO.BOARD map PIN numbers like on BOARD.
    # GPIO.BCM map PIN numbers like in documentation.
    GPIO.setmode(GPIO.BOARD)  # Setting PIN numbers context.
    GPIO.setwarnings(False)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    GPIO.add_event_detect(echo_pin, GPIO.BOTH, callback=handle_echo_pin_change)

    # Set trigger to False (Low)
    GPIO.output(trigger_pin, False)

    # Allow module to settle
    time.sleep(SENSOR_SETTLE_TIME)

    try:
        while True:
            distance = run_ultrasonic_sensor(trigger_pin, echo_pin)
            print("Ultrasonic Measurement - Distance: " + str(distance) + " cm")
            # TODO: Send distance value via event bus

            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print("End by user keyboard interrupt")
    finally:
        GPIO.cleanup()
        sys.exit(0)


if __name__ == '__main__':
    # Define global variables for the sensor
    echo_start = 0
    echo_stop = 0

    # Run module
    main()
