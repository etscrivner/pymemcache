# -*- coding: utf-8 -*-
"""
    pymemcache.cli
    ~~~~~~~~~~~~~~
    Command-line interface (CLI) for pymemcache

"""
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
    configure_logging()
    server.serve_forever()
