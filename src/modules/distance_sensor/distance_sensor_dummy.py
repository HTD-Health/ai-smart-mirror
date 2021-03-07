# Import required Python libraries
import time
import argparse
import sys
import zmq
import xdrlib


def main():
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser()

    # Set arguments
    parser.add_argument('--sleep', type=float, default=0.1, help='Sleep time between distance measurements.')
    parser.add_argument('--port', default="5555", help='Port to which connect to')
    parser.add_argument('--topic', type=int, default=10001, help='Event bus topic for the distance sensor')
    parser.add_argument('--thresholddistance', type=int, default=80, help='Threshold distance under which sensor '
                                                                          'will fire an event.')
    parser.add_argument('--sensorsettletime', type=float, default=0.3, help='Time for the sensor to settle after '
                                                                            'setting the Trigger pin to the LOW state')
    parser.add_argument('--hadrcodeddistance', type=float, default=60, help='Hardcoded value that will be used '
                                                                            'instead of sensor readouts')

    # Get command line arguments
    init_args = parser.parse_args()
    sleep_time = init_args.sleep
    port = init_args.port
    topic = init_args.topic
    threshold_distance = init_args.thresholddistance
    sensor_settle_time = init_args.sensorsettletime
    hardcoded_sensor_distance = init_args.hadrcodeddistance

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:%s" % port)
    data_packer = xdrlib.Packer()

    print("Ultrasonic Measurement. Dummy set for the distance: " + str(hardcoded_sensor_distance) + "cm")

    # Allow module to settle
    time.sleep(sensor_settle_time)

    try:
        while True:
            # Hardcode distance value
            distance = hardcoded_sensor_distance
            print("Ultrasonic Measurement - Distance: " + str(distance) + " cm")

            # Send event if measured distance is less than set threshold
            if distance <= threshold_distance:
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
        sys.exit(0)


if __name__ == '__main__':
    # Run module
    main()
