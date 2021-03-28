# Import required Python libraries
import time
import argparse
import sys
import zmq
import xdrlib
import logging

logger = logging.getLogger(__name__)


def main():
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser()

    # Set arguments
    parser.add_argument('--sleep', type=float, default=0.1, help='Sleep time between distance measurements.')
    parser.add_argument('--port', default="5555", help='Port to which connect to')
    parser.add_argument('--topic', type=int, default=10001, help='Event bus topic for the distance sensor')
    parser.add_argument('--hostname', type=str, default='tcp://127.0.0.1', help='Hostname address')
    parser.add_argument('--sensorsettletime', type=float, default=0.3, help='Time for the sensor to settle after '
                                                                            'setting the Trigger pin to the LOW state')
    parser.add_argument('--hadrcodeddistance', type=float, default=60, help='Hardcoded value that will be used '
                                                                            'instead of sensor readouts')
    parser.add_argument('--loglevel', default="WARNING", help='Sets log level - what messages are printed out')

    # Get command line arguments
    init_args = parser.parse_args()
    sleep_time = init_args.sleep
    port = init_args.port
    topic = init_args.topic
    hostname = init_args.hostname
    sensor_settle_time = init_args.sensorsettletime
    hardcoded_sensor_distance = init_args.hadrcodeddistance
    log_level = init_args.loglevel

    logging.basicConfig(level=log_level.upper())

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(f"{hostname}:{port}")
    data_packer = xdrlib.Packer()

    logger.info(f"Ultrasonic Measurement. Dummy set for the distance: {hardcoded_sensor_distance} cm")

    # Allow module to settle
    time.sleep(sensor_settle_time)

    try:
        while True:
            logger.info(f"Ultrasonic Measurement - Distance: {hardcoded_sensor_distance} cm")

            # Send event with the hardcoded distance
            data_packer.pack_uint(topic)
            data_packer.pack_float(hardcoded_sensor_distance)
            socket.send(data_packer.get_buffer())
            data_packer.reset()

            time.sleep(sleep_time)
    except KeyboardInterrupt:
        logger.info("End by user keyboard interrupt")
    except Exception as e:
        print(e)
    finally:
        sys.exit(0)


if __name__ == '__main__':
    # Run module
    main()
