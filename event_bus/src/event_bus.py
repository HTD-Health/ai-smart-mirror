import asyncio
import argparse
import logging

import zmq
from zmq.asyncio import Context

ctx = Context.instance()
logger = logging.getLogger(__name__)


async def main(port_in: str, port_out: str):
    """ Create distribution core

    Args:
        port_in (str): Port that bus is listening on for new events
        port_out (str): Port on which events are distributed to other components
    """
    logger.info(f'Listening on {port_in=} and {port_out=}')
    socket_in = ctx.socket(zmq.SUB)
    socket_out = ctx.socket(zmq.PUB)
    socket_in.bind("tcp://*:%s" % port_in)
    socket_out.bind("tcp://*:%s" % port_out)
    socket_in.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        msg = await socket_in.recv()
        logger.debug('Got message')
        await socket_out.send(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Event bus server')
    parser.add_argument(
        '--port_in',
        default="5555",
        help='Port on which server listens for events'
    )
    parser.add_argument(
        '--port_out',
        default="5556",
        help='Port on which server propagates for events'
    )
    parser.add_argument(
        '--log_level',
        default="WARNING",
        help='Sets log level - what messages are printed out'
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level.upper())
    asyncio.run(
        main(args.port_in, args.port_out)
    )
