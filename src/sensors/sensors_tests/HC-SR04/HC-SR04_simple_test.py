# Code based (a lot) on code from https://github.com/makersdigest/T07-HC-SR04-Ultrasonic-Sensor
# Imports python modules
import RPi.GPIO as GPIO
import time
import sys
import argparse


def run_hc_sr04(trigger_pin, echo_pin):
    try:
        while True:
			# "Warm up" trigger pin...
            GPIO.output(trigger_pin, GPIO.LOW)           # Set pin to LOW
            time.sleep(2)                                # Wait 2 seconds
			
            GPIO.output(trigger_pin, GPIO.HIGH)          # Set pin to HIGH
            time.sleep(0.0001)                           # wait 10 microseconds (10us HIGH pulse)
            GPIO.output(trigger_pin, GPIO.LOW)           # Set pin to LOW (End 10us HIGH pulse)
			
			# Measure distance
            while GPIO.input(echo_pin) == 0:             # wait for input from echo. if LOW record time
                pulse_start = time.time()
            while GPIO.input(echo_pin) == 1:             # wait for input from echo. if HIGH record time
                pulse_end = time.time()

			# Calculating the distance
            duration = pulse_end - pulse_start           # Calculate time difference
            inches = (duration / 2) * 13503.9            # Convert to inches
            cm = (duration / 2) * 343 * 100              # Convert to centimeters

            # Display output to user.
            print('in: %0.2f\tcm: %0.2f' % (inches, cm))

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)


if __name__ == '__main__':
	# Creates Argument Parser object named parser
    parser = argparse.ArgumentParser()
	
	# Argument 1: Trigger output pin
    parser.add_argument('--trig', type=int, default=7,
                        help='PIN with TRIGGER output PIN.')

    # Argument 2: Echo input pin
    parser.add_argument('--echo', type=int, default=11,
                        help='PIN with ECHO input PIN.')

	# Get command line arguments
	init_args = parser.parse_args()
	trigger_pin = init_args.trig
	echo_pin = init_args.echo
	
	print('Setting up GPIO...')
	GPIO.setmode(GPIO.BOARD)			# Setting PIN numbers context. GPIO.BOARD map PIN numbers like on BOARD. GPIO.BCM map PIN numbers like in docummentation.
	GPIO.setup(trigger_pin, GPIO.OUT)
	GPIO.setup(echo_pin, GPIO.IN)
						
    run_hc_sr04(trigger_pin, echo_pin)
    sys.exit(0)
sys.exit(0)
