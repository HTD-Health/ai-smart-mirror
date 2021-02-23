#!/usr/bin/python
# Import required Python libraries
import time
import argparse
import sys
import zmq
import xdrlib

import RPi.GPIO as GPIO

# Consts that don't need to be set from the outside
SPEED_OF_SOUND = 34300  # cm/s
HALF_SPEED_OF_SOUND = SPEED_OF_SOUND / 2
TRIGGER_PULSE_TIME = 0.00001  # Needs to be 10us pulse to trigger the sensor
SENSOR_SETTLE_TIME = 0.3  # Time for the sensor to settle after setting the Trigger pin to the LOW state


class DistanceSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.echo_start = 0
        self.echo_stop = 0

    def send_trigger(self):
        # Send pulse to trigger
        GPIO.output(self.trigger_pin, True)
        time.sleep(TRIGGER_PULSE_TIME)
        GPIO.output(self.trigger_pin, False)

    def handle_echo_pin_change(self, channel):
        # Check if the pin is in High or Low state
        if GPIO.input(channel):
            self.echo_start = time.time()
        else:
            self.echo_stop = time.time()

    def measure_distance(self):
        self.send_trigger()

        # Calculate pulse length
        pulse_duration = self.echo_stop - self.echo_start
        calculated_distance = round(pulse_duration * HALF_SPEED_OF_SOUND, 2)

        return calculated_distance


def main():
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser()

    # Set arguments
    parser.add_argument('--trig', type=int, default=16, help='PIN with TRIGGER output PIN.')
    parser.add_argument('--echo', type=int, default=18, help='PIN with ECHO input PIN.')
    parser.add_argument('--sleep', type=float, default=0.1, help='Sleep time between distance measurements.')
    parser.add_argument('--port', default="5555", help='Port to which connect to')
    parser.add_argument('--topic', type=int, default=10001, help='Event bus topic for the distance sensor')

    # Get command line arguments
    init_args = parser.parse_args()
    trigger_pin = init_args.trig
    echo_pin = init_args.echo
    sleep_time = init_args.sleep
    port = init_args.port
    topic = init_args.topic

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:%s" % port)
    data_packer = xdrlib.Packer()

    print("Ultrasonic Measurement. Setting up GPIO...")

    # GPIO.BOARD map PIN numbers like on BOARD.
    # GPIO.BCM map PIN numbers like in documentation.
    GPIO.setmode(GPIO.BOARD)  # Setting PIN numbers context.
    GPIO.setwarnings(False)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    distance_sensor = DistanceSensor(trigger_pin, echo_pin)

    GPIO.add_event_detect(echo_pin, GPIO.BOTH, callback=distance_sensor.handle_echo_pin_change)

    # Set trigger to False (Low)
    GPIO.output(trigger_pin, False)

    # Allow module to settle
    time.sleep(SENSOR_SETTLE_TIME)

    try:
        while True:
            distance = distance_sensor.measure_distance()
            print("Ultrasonic Measurement - Distance: " + str(distance) + " cm")

            data_packer.pack_uint(topic)
            data_packer.pack_float(distance)
            socket.send(data_packer.get_buffer())
            data_packer.reset()

            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("End by user keyboard interrupt")
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
        sys.exit(0)


if __name__ == '__main__':
    # Run module
    main()
