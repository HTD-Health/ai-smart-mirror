import argparse
import time
import zmq
import xdrlib


def main(host, port, topic, data):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://%s:%s" % (host, port))
    data_packer = xdrlib.Packer()
    data_packer.pack_uint(topic)
    data_packer.pack_bytes(data.encode('utf-8'))
    # give some time to connect
    time.sleep(1)
    print(f'sending: {data_packer.get_buffer()}')
    socket.send(data_packer.get_buffer())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send Event to bus server')
    parser.add_argument(
        '--port',
        default="5555",
        help='Port to which connect to'
    )
    parser.add_argument(
        'topic',
        type=int,
        help='topic id'
    )
    parser.add_argument(
        'data',
        help='data to be send to topic'
    )
    args = parser.parse_args()
    main('127.0.0.1', args.port, args.topic, args.data)
