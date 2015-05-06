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


logger = logging.getLogger(__name__)


def configure_logging():
    """Configure logging for this application"""
    root_logger = logging.getLogger(0)
    root_logger.setLevel(logging.DEBUG)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(stderr_handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Memcached implementation in python')
    parser.add_argument('--host', type=str, default='localhost',
                        help='An IP address or hostname')
    parser.add_argument('--port', type=int, default=9999,
                        help='A TCP port to listen for connections on')
    results = parser.parse_args()

    configure_logging()
    server.serve_forever(host=results.host, port=results.port)
