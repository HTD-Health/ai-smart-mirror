import argparse
import logging
import os
import xdrlib

import zmq

from src.detector.code.model_loader import model_loader

IMAGE_CAPTURED = 2
PIC_DIRECTORY = '/tmp/images/'
MODEL_DIRECTORY = '/tmp/models/'

logger = logging.getLogger(__name__)


def main(
        event_bus_server,
        receiving_port,
        topic_distance,  # Load event bus module configuration
        model_dir,
        image_dir,
        **kwargs
) -> None:
    """
    Waiting for message from camera. On message suitable value check image with the network model.
    """
    # PREPARATION
    # Check if model directory exist
    if not os.path.exists(model_dir):
        raise FileExistsError("Given directory do not exist. Directory: ", model_dir)
    # Check if image directory exist
    if not os.path.exists(image_dir):
        raise FileExistsError("Given directory do not exist. Directory: ", image_dir)
    # Load model
    neural_model = model_loader(model_dir)
    neural_model.eval()

    # EVENT BUS
    # Connections and sockets preparation
    # Create socket from where we will be consuming signals
    context = zmq.Context.instance()

    # Create object to pack data
    data_packer = xdrlib.Packer()
    # Pack topic filter for distance into a buffer to be able to catch it from incoming messages
    data_packer.pack_uint(topic_distance)

    # Subscribe for message from camera to certain socket
    consume_socket = context.socket(zmq.SUB)
    consume_socket.setsockopt(zmq.SUBSCRIBE, data_packer.get_buffer())
    # Connect to event bus server to receive
    received_url = f"tcp://{event_bus_server}:{receiving_port}"
    consume_socket.connect(received_url)

    data_packer = xdrlib.Packer()
    data_unpacker = xdrlib.Unpacker(b'')

    # MODEL
    logger.info(f'Model ready, listening for events: {topic_distance} from {received_url}')
    # Main loop
    while True:
        # Waiting for any message
        msg = consume_socket.recv()
        logger.info(f'received msg {msg}')
        # Pass message to unpacking object
        data_unpacker.reset(msg)

        # Load image
        image_path = image_dir + msg

        # Run model
        result = neural_model(image_path)

        # Print result
        result_text = f'Image {msg} has been classified as {result}'
        print(result_text)
        logger.info(result_text)


if __name__ == "__main__":
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser(description='Detector server')

    # Set arguments
    parser.add_argument(
        '--event_bus_server',
        default="127.0.0.1",
    )
    parser.add_argument(
        '--port_in',
        default="5556",
        help='Port on which app listens for events'
    )
    parser.add_argument(
        '--topic_in',
        type=int,
        default=IMAGE_CAPTURED,
    )
    parser.add_argument(
        '--log_level',
        default="INFO",
        help='Sets log level - what messages are printed out'
    )
    parser.add_argument(
        '--image_dir',
        default=PIC_DIRECTORY,
        help='Captured images output directory'
    )
    parser.add_argument(
        '--model_dir',
        default=MODEL_DIRECTORY,
        help='Saved model directory'
    )
    args = parser.parse_args()

    # Setting logger
    logging.basicConfig(
        level=args.log_level.upper()
    )

    # Run module
    main(
        event_bus_server=args.event_bus_server,
        receiving_port=args.port_in,
        topic_distance=args.topic_in,
        model_dir=args.image_dir,
        image_dir=args.image_dir
    )
