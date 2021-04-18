import argparse
import time
import zmq
import xdrlib


def main(host, port, topic, data):
    """
    Sending events to the specific topic after connecting to the host.

    Parameters:
        host (str): host name to connect.
        port (str): port of the host to connect.
        topic (int): ID of topic to subscribe.
        data (str): data to be send to topic.
    """
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
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser(description='Send Event to bus server')

    # Set arguments
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

    # Run module
    main('127.0.0.1', args.port, args.topic, args.data)
