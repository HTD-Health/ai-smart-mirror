# https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html
# https://learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/

import argparse
import zmq
import random
import sys
import time
import xdrlib
import numpy as np

DTYPES = {
    'int64': 1,
    'float64': 2
}


def main(port, sleep_time):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:%s" % port)
    data_packer = xdrlib.Packer()

    while True:
        topic = random.randrange(9999,10005)
        data_array = np.random.rand(3,2)
        data_packer.pack_uint(topic)
        data_packer.pack_array(data_array.shape, data_packer.pack_uint)
        data_packer.pack_uint(DTYPES[data_array.dtype.name])
        data_packer.pack_bytes(data_array.tobytes())
        print('sending')
        print(topic)
        print(data_array)
        socket.send(data_packer.get_buffer())
        data_packer.reset()
        time.sleep(float(sleep_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Event bus server')
    parser.add_argument(
        '--port',
        default="5555",
        help='Port to which connect to'
    )
    parser.add_argument(
        '--sleep_time',
        default="1.0",
        help='How long wait between events (in seconds)'
    )
    args = parser.parse_args()
    main(args.port, args.sleep_time)
