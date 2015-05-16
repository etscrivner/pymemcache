# -*- coding: utf-8 -*-
"""
    pymemcache.server
    ~~~~~~~~~~~~~~~~~
    Interfaces for serving memcached server over TCP.

"""
import logging
import socket

from pymemcache import cache
from pymemcache import request


logger = logging.getLogger(__name__)


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


def slurp_connection(connection, client_address):
    """Get all data being sent over the given connection.

    :param connection: A connection
    :type connection: socket.connection
    :param client_address: The host and port address tuple
    :type client_address: tuple
    :rtype: str or unicode
    """
    raw_request_data = ""
    last = connection.recv(4096)
    while last:
        raw_request_data += last
        last = connection.recv(4096)
    return raw_request_data


def process_command(raw_data, the_cache):
    """Process the command associated with the given raw data.

    :param raw_data: The raw data from the socket
    :type raw_data: str or unicode
    :param the_cache: The cache for this process
    :type the_cache: dict
    :rtype: str or unicode
    """
    raw_data = raw_data.decode('utf-8')
    command, body = request.parse_command(raw_data)
    logger.debug('--> Command %r', command)
    if command.startswith('get'):
        key = command.split(' ')[1]
        return the_cache.get(key) or '-1'
    if command.startswith('set'):
        key = command.split(' ')[1]
        the_cache.set(key, body[0])
        return '1'


def serve_forever(host='localhost', port=9999):
    """Process incoming requests from the given socket.

    :param host: The host to serve on
    :type host: str or unicode
    :param port: The port to listen on
    :type port: int
    """
    sock = create_server_socket(host, port)
    process_cache = cache.Cache({u'\u00e9poche': 'Got it!'})
    try:
        sock.listen(1)
        logger.info('--> Accepting connections on %s:%d', host, port)
        while True:
            connection, client_address = sock.accept()
            try:
                logger.info('--> Connection from %r', client_address)
                raw_data = slurp_connection(connection, client_address)
                result = process_command(raw_data, process_cache)
                logger.info('--> Result "%r"', result)
                connection.send(result)
            finally:
                logger.info('--> Connection closed.')
                connection.close()
    except KeyboardInterrupt:
        logger.info('Shutting down')
