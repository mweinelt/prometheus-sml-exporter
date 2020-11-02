import asyncio

import click
from prometheus_client import start_http_server
from sml.asyncio import SmlProtocol

from . import SmlExporter

@click.command()
@click.argument('tty', default='/dev/ttyUSB0')
@click.option('--http-port', '-p', default=9999)
def main(tty, http_port):
    handler = SmlExporter()
    proto = SmlProtocol(tty)
    proto.add_listener(handler.event, ['SmlGetListResponse'])
    start_http_server(http_port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(proto.connect(loop))
    loop.run_forever()


