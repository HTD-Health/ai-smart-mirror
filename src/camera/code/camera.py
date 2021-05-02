import argparse
import logging
import time
import xdrlib
import os
import uuid

import zmq

from pathlib import Path

try:
    import picamera
    CAMERA_IMPLEMENTATION = 'picamera'
except (ImportError, OSError):
    import cv2
    CAMERA_IMPLEMENTATION = 'cv2'

SOMEONE_VISIBLE = 1
IMAGE_CAPTURED = 2
PIC_DIRECTORY = '/tmp/'


logger = logging.getLogger(__name__)


if CAMERA_IMPLEMENTATION == 'cv2':
    class CameraInterface:
        """
        Class for handling camera device using OpenCV library.
        """
        def __init__(self, height: int, width: int):
            self.height = height
            self.width = width
            self.camera = cv2.VideoCapture(0) # Number which capture webcam in my machine
            # Camera warm-up time
            time.sleep(2)

        def capture(self, filename: str):
            """
            Take a snapshot from the camera and save the captured image under a given name.

            Parameters:
                filename (str): name of the file with captured image.
            """
            check, frame = self.camera.read()
            resized_frame = cv2.resize(frame, (self.width, self.height), )
            cv2.imwrite(filename=filename, img=resized_frame)

        def close(self):
            """
            Closes video file or capturing device.
            """
            if self.camera:
                self.camera.release()


if CAMERA_IMPLEMENTATION == 'picamera':
    class CameraInterface:
        """
        Class for handling camera device using picamera library.
        """
        def __init__(self, height: int, width: int):
            self.height = height
            self.width = width
            self.camera = picamera.PiCamera()
            self.camera.resolution = (self.width, self.height)
            self.camera.start_preview()
            # Camera warm-up time
            time.sleep(2)

        def capture(self, filename: str):
            """
            Take a snapshot from the camera and save the captured image under a given name.

            Parameters:
                filename (str): name of the file with captured image.
            """
            self.camera.capture(filename)

        def close(self):
            """
            Closes video file or capturing device.
            """
            if self.camera:
                self.camera.close()


class ActiveCamera:
    """
    Class implementing one of the possible camera handling interfaces.
    """
    def __init__(self, height: int, width: int):
        self.camera = CameraInterface(height, width)

    def __enter__(self):
        return self.camera

    def __exit__(self, *args, **kwargs):
        if self.camera:
            self.camera.close()


def main(
        camera,
        image_format,
        image_dir,
        # event bus
        event_bus_server,
        receiving_port,
        sending_port,
        # Load event bus module configuration
        topic_distance,
        topic_camera,
        **kwargs
) -> None:
    """
    Waiting for message from distance sensor. On message suitable value take snap from camera and broadcast it.
    """
    # prepare directory
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    # Connections and sockets preparation
    # Create socket from where we will be consuming signals
    context = zmq.Context.instance()

    # Create object to pack data
    data_packer = xdrlib.Packer()
    # Pack topic filter for distance into a buffer to be able to catch it from incoming messages
    data_packer.pack_uint(topic_distance)

    # Subscribe for message from distance sensor to certain socket
    consume_socket = context.socket(zmq.SUB)
    consume_socket.setsockopt(zmq.SUBSCRIBE, data_packer.get_buffer())
    # Connect to event bus server to receive
    received_url = f"tcp://{event_bus_server}:{receiving_port}"
    consume_socket.connect(received_url)

    # Create socket on where we will be producing signals
    produce_socket = context.socket(zmq.PUB)
    # Connect to event bus server to send
    produce_url = f"tcp://{event_bus_server}:{sending_port}"
    produce_socket.connect(produce_url)

    data_packer = xdrlib.Packer()
    data_unpacker = xdrlib.Unpacker(b'')

    with camera as active_camera:
        logger.info(f'camera ready, listening for events: {topic_distance} from {received_url}')
        # Main loop
        while True:
            # Waiting for any message
            msg = consume_socket.recv()
            logger.info(f'received msg {msg}')
            # Pass message to unpacking object
            data_unpacker.reset(msg)

            # Prepare file name
            snap_name = f'{time.time()}.{uuid.uuid4()}.{image_format}'

            # Take a snap and remember image name
            active_camera.capture(
                os.path.join(
                    image_dir,
                    snap_name
                )
            )
            # Pack topic and file name to send
            data_packer.pack_uint(topic_camera)
            data_packer.pack_string(snap_name.encode('utf-8'))

            logger.info(f'broadcasting topic: {topic_camera} with value: {snap_name} to {produce_url}')

            # Send data
            produce_socket.send(data_packer.get_buffer())
            data_packer.reset()


if __name__ == "__main__":
    # Creates Argument Parser object named parser
    parser = argparse.ArgumentParser(description='Camera server')

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
        '--port_out',
        default="5555",
        help='Port on which app sends new events'
    )
    parser.add_argument(
        '--topic_in',
        type=int,
        default=SOMEONE_VISIBLE,
    )
    parser.add_argument(
        '--topic_out',
        type=int,
        default=IMAGE_CAPTURED,
    )
    parser.add_argument(
        '--log_level',
        default="INFO",
        help='Sets log level - what messages are printed out'
    )
    parser.add_argument(
        '--image_height',
        type=int,
        default=768
    )
    parser.add_argument(
        '--image_width',
        type=int,
        default=1024
    )
    parser.add_argument(
        '--image_format',
        default='jpg'
    )
    parser.add_argument(
        '--image_dir',
        default=PIC_DIRECTORY,
        help='Captured images output directory'
    )
    args = parser.parse_args()

    # Setting logger
    logging.basicConfig(
        level=args.log_level.upper()
    )

    camera = ActiveCamera(
        width=args.image_width,
        height=args.image_height,
    )

    # Run module
    main(
        camera=camera,
        image_dir=args.image_dir,
        image_format=args.image_format,
        event_bus_server=args.event_bus_server,
        topic_camera=args.topic_out,
        topic_distance=args.topic_in,
        sending_port=args.port_out,
        receiving_port=args.port_in,
    )
