import asyncio
import zmq
from zmq.asyncio import Context
import xdrlib
import numpy as np

ctx = Context.instance()
data_packer = xdrlib.Packer()
data_unpacker = xdrlib.Unpacker(b'')

DTYPES = {
    1: np.int64,
    2: np.float64,
}


async def main():
    """
    Create consumer core.
    """
    consumer_socket = ctx.socket(zmq.SUB)
    topic_filter = 10001
    data_packer.pack_uint(topic_filter)
    consumer_socket.setsockopt(zmq.SUBSCRIBE, data_packer.get_buffer())
    consumer_socket.connect('tcp://127.0.0.1:5556')
    while True:
        msg = await consumer_socket.recv()
        data_unpacker.reset(msg)
        topic = data_unpacker.unpack_uint()
        if topic == 10001:
            array_shape = data_unpacker.unpack_array(data_unpacker.unpack_uint)
            array_data_type = data_unpacker.unpack_uint()
            data = data_unpacker.unpack_bytes()
            arr = np.frombuffer(
                data,
                dtype=DTYPES[array_data_type]
            ).reshape(array_shape)
            print('received')
            print(topic)
            print(arr)
    consumer_socket.close()

asyncio.run(main())
