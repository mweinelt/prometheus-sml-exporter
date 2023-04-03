import asyncio
import logging

import click
from prometheus_client import start_http_server
from sml.asyncio import SmlProtocol  # type: ignore

from . import SmlExporter, logger


@click.command()
@click.argument("tty", type=click.Path(exists=True))
@click.option(
    "--http-port",
    "-p",
    type=click.IntRange(1024, 65535),
    default=9761,
    show_default=True,
    help="HTTP Port for the Prometheus Exporter",
)
@click.option("--verbose/--no-verbose", "-v", default=False)
def main(tty: str, http_port: int, verbose: bool) -> None:
    logging.basicConfig()
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handler = SmlExporter()
    proto = SmlProtocol(tty)
    proto.add_listener(handler.event, ["SmlGetListResponse"])
    start_http_server(http_port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(proto.connect(loop))
    loop.run_forever()
