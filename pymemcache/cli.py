# -*- coding: utf-8 -*-
"""
    pymemcache.cli
    ~~~~~~~~~~~~~~
    Command-line interface (CLI) for pymemcache

"""
import argparse
import logging
import sys

from pymemcache import server


LOGGER = logging.getLogger(__name__)


def configure_logging():
    """Configure logging for this application"""
    root_logger = logging.getLogger(0)
    root_logger.setLevel(logging.DEBUG)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(stderr_handler)


def run():
    """Run command-line server interface"""
    parser = argparse.ArgumentParser(
        description='Memcached implementation in python')
    parser.add_argument('--port', type=int, default=9999,
                        help='A TCP port to listen for connections on')
    results = parser.parse_args()

    configure_logging()
    server.serve_forever(port=results.port)


if __name__ == '__main__':
    run()
