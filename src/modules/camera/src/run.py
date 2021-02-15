import xdrlib

import zmq
from zmq.asyncio import Context

from src.modules.camera.src.camera_snap import camera_snap
from src.utils.config_loader import load_config_file


async def main() -> None:
    """
    Waiting for message from distance sensor. On message suitable value take snap from camera and broadcast it.
    """
    # Connections and sockets preparation
    # Create socket from where we will be consuming signals
    instance_context = Context.instance()
    consume_socket = instance_context.socket(zmq.SUB)

    # Subscribe for message from distance sensor to certain socket
    consume_socket.setsockopt(zmq.SUBSCRIBE, "{0:b}".format(topic_distance))

    # Connect to event bus server to receive
    consume_socket.connect(event_bus_server_ip, ":%s" % receiving_port)

    # Create socket on where we will be producing signals
    zmq_context = zmq.Context()
    produce_socket = zmq_context.socket(zmq.PUB)

    # Connect to event bus server to send
    produce_socket.connect(event_bus_server_ip, ":%s" % sending_port)

    # Create object to pack data
    data_packer = xdrlib.Packer()

    # Pack topic filter for distance into a buffer to be able to catch it from incoming messages
    data_packer.pack_uint(topic_distance)

    # Main loop
    while True:
        # Waiting for any message
        msg = await consume_socket.recv()

        # Create object to unpack data. Treat passed data as bits
        data_unpacker = xdrlib.Unpacker(b'')

        # Pass message to unpacking object
        data_unpacker.reset(msg)

        # Get topic
        topic = data_unpacker.unpack_uint()

        # Proceed with actions if the message is from the distance sensor
        if topic == topic_distance:
            # Unpack message from distance sensor
            distance_sensor_signal = data_unpacker.unpack_float()

            # Check if we object is enough close to take snap
            if distance_sensor_signal <= border_distance:
                # Take a snap and remember image name
                image_file_name = camera_snap()

                # Pack topic and file name to send
                data_packer.pack_uint(topic_camera)
                data_packer.pack_string(image_file_name)

                print('BROADCASTING TOPIC: ', topic_camera, " WITH VALUE: ", image_file_name)

                # Send data
                produce_socket.send(data_packer.get_buffer())
                data_packer.reset()

if __name__ == "__main__":
    # Get configuration data
    config_data = load_config_file()

    # Load event bus general configuration
    event_bus_server_ip = config_data["event_bus"]["event_bus_server_ip"]
    receiving_port = config_data["event_bus"]["receiving_port"]
    sending_port = config_data["event_bus"]["sending_port"]

    # Load event bus module configuration
    topic_distance = config_data["distance_sensor"]["event_bus"]["topic"]
    topic_camera = config_data["camera"]["event_bus"]["topic"]

    # Load module logic
    border_distance = config_data["camera"]["module_logic"]["border_distance"]

    # Run module
    main()
