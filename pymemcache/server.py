# -*- coding: utf-8 -*-
"""
    pymemcache.server
    ~~~~~~~~~~~~~~~~~
    Interfaces for serving memcached server over TCP.

"""
import logging
import socket

from pymemcache import cache
from pymemcache import interactors
from pymemcache import utils


LOGGER = logging.getLogger(__name__)


def create_server_socket(host, port):
    """Create a server socket bound to the given host and port.

    :param host: A host
    :type host: str or unicode
    :param port: A port
    :type port: int
    :return: A fresh server socket bound to the host and port
    :rtype: socket.socket
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid address already in use errors on multiple runs
    # http://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    return sock


def serve_forever(host='localhost', port=9999):
    """Process incoming requests from the given socket.

    :param host: The host to serve on
    :type host: str or unicode
    :param port: The port to listen on
    :type port: int
    """
    sock = create_server_socket(host, port)
    # The cache for this process
    process_cache = cache.Cache({u'\u00e9poche': 'Got it!'})
    try:
        sock.listen(1)
        LOGGER.info('--> Accepting connections on %s:%d', host, port)
        while True:
            connection, client_address = sock.accept()
            try:
                LOGGER.info('--> Connection from %r', client_address)
                raw_data = utils.slurp_connection(connection)
                resp = interactors.execute_request(raw_data, process_cache)
                LOGGER.info('--> Result "%r"', resp.data)
                resp.send_via(connection)
            finally:
                LOGGER.info('--> Connection closed.')
                connection.close()
    except KeyboardInterrupt:
        LOGGER.info('Shutting down')
