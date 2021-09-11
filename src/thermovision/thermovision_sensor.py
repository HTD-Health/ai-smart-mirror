#!/usr/bin/env python3

# Import required Python libraries
import argparse
import logging
import math
import numpy as np
import seeed_mlx9064x
import sys
import xdrlib
import zmq

logger = logging.getLogger(__name__)

class ThermovisionSensor:
    """
    The class that supports a thermal imaging camera sensor

    For the configuration of the raspberry pi and the mxl90641 sensor,
    the maximum value of the sensor refresh is 8 HZ.

    Attributes:
        size_x(int): sensor resolution in horizontal pixels
        size_y(int): sensor resolution in vertical pixels
    """
    def __init__(self):
        self.mlx = seeed_mlx9064x.grove_mxl90641()
        self.mlx.refresh_rate = seeed_mlx9064x.RefreshRate.REFRESH_8_HZ
        self.horizontal_size = 16
        self.vertical_size = 12

    def get_frame(self):
        """
        Returns a list of temperature values (in degrees Celsius) for each pixel
        ex: [24.47631779730409, 24.225540060143487, ..., 24.225540060143487]

        """
        try:
            frame = [0] * self.horizontal_size * self.vertical_size
            self.mlx.getFrame(frame)
            print(frame)
            return frame
        except ValueError:
            return None

    def get_temperature(self):
        """
        Returns the average temperature for human temperature measurement
        at a very close distance of max 10 cm
        
        In the event that the measured surface does not use all pixels,
        we filter values in the range of 32-40 degrees Celsius to increase the accuracy.
        """
        measurement_points = self.get_frame()

        if measurement_points == None:
            return np.nan
        measurement_points = list(filter(lambda temp: 32 < float(temp) < 40, measurement_points))
        return np.average(measurement_points)
    

def main():
    """
    The function determines the sensor and connects to the event bus.

    Upon receiving a query on port 5557,
    it will return the temperature of the object on port 5555
    """  
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser()

    # Set arguments
    parser.add_argument('--event_bus_server', default="127.0.0.1",)
    parser.add_argument('--port_in', default="5557", help='Port on which app listens for events')
    parser.add_argument('--topic_in', type=int, default=20001, help='Event bus topic for trigger the thermovision sensor')
    parser.add_argument('--port_out', default="5555", help='Port to which connect to')
    parser.add_argument('--topic_out', type=int, default=20002, help='Event bus topic for the thermovision sensor')
    parser.add_argument('--log_level', default="WARNING", help='Sets log level - what messages are logger.infoed out')

    # Get command line arguments
    init_args = parser.parse_args()
    port_out = init_args.port_out
    topic_out = init_args.topic_out
    port_in = init_args.port_in
    topic_in = init_args.topic_in
    event_bus_server = init_args.event_bus_server
    log_level = init_args.log_level

    logging.basicConfig(level=log_level.upper())

    produce_url = f"tcp://{event_bus_server}:{port_out}"
    logger.info(f'Thermovision sensor ready, producing events to : {topic_out} on {produce_url}')

    trigger_url = f"tcp://{event_bus_server}:{port_in}"
    logger.info(f'Thermovision sensor ready for trigger to : {topic_in} on {trigger_url}')

    context = zmq.Context()
    data_packer = xdrlib.Packer()
    data_packer.pack_uint(topic_in)
    data_unpacker = xdrlib.Unpacker(b'')

    produce_socket = context.socket(zmq.PUB)
    produce_socket.connect(produce_url)

    consume_socket = context.socket(zmq.SUB)
    consume_socket.setsockopt(zmq.SUBSCRIBE, data_packer.get_buffer())
    consume_socket.connect(trigger_url)

    thermal_sensor = ThermovisionSensor()

    try:
        while True:
            # Waiting for any message
            print("while")
            msg = consume_socket.recv()
            print("msg")
            logger.info(f'received msg {msg}')
            # Pass message to unpacking object
            data_unpacker.reset(msg)

            # Take a measurement
            temperature = thermal_sensor.get_temperature()
            logger.debug(f"Thermovision Measurement - Temperature: {temperature} °C")

            # Send a temperature
            data_packer.pack_uint(topic_out)
            data_packer.pack_float(temperature)
            produce_socket.send(data_packer.get_buffer())
            data_packer.reset()  
    except KeyboardInterrupt:
        logger.warning("End by user keyboard interrupt")
        sys.exit(0)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
