# -*- coding: utf-8 -*-
"""
    pymemcache.utils
    ~~~~~~~~~~~~~~~~
    Miscellaneous utility methods

"""
import errno
import logging
import socket
import time

import six

from pymemcache import errors


LOGGER = logging.getLogger(__name__)


def slurp_connection(connection):
    """Get all data being sent over the given connection.

    :param connection: A connection
    :type connection: socket.connection
    :rtype: str or unicode
    """
    raw_request_data = six.binary_type()

    while True:
        try:
            raw_request_data = connection.recv(4096)
        except socket.error as sockerr:
            err = sockerr.args[0]
            if err in [errno.EAGAIN, errno.EWOULDBLOCK]:
                time.sleep(1)
                continue
        else:
            return raw_request_data.decode('utf-8')


def spit_connection(connection, data):
    """Send all of the given data over connection.

    :param connection: A socket connection
    :type connection: socket.socket
    """
    total_sent = 0

    while total_sent < len(data):
        sent = connection.send(data[total_sent:])

        if sent == 0:
            raise errors.ConnectionError('Socket connection broken.')

        total_sent += sent
