# -*- coding: utf-8 -*-
"""
    pymemcache.server
    ~~~~~~~~~~~~~~~~~
    Interfaces for serving memcached server over TCP.

"""
import logging

from twisted.internet import endpoints
from twisted.internet import error
from twisted.internet import protocol
from twisted.internet import reactor

from pymemcache import cache
from pymemcache import interactors


LOGGER = logging.getLogger(__name__)


class MemcachedProtocol(protocol.Protocol):
    """Represents the memcached protocol"""

    def __init__(self, process_cache):
        """Initialized memcached protocol.

        :param process_cache: The process cache
        :type process_cache: pymemcache.cache.Cache
        """
        self.cache = process_cache

    def connectionMade(self):
        """Handle when a new connection comes in"""
        peer = self.transport.getPeer()
        LOGGER.debug(
            '--> Received new connection from %s:%d',
            peer.host, peer.port
        )

    def connectionLost(self, reason=error.ConnectionDone):
        """Handle when a connection is lost"""
        LOGGER.debug('--> Connection dropped %r.', reason)

    def dataReceived(self, data):
        """Handle reception of data across the transport.

        :param data: The data received
        :type data: mixed
        """
        LOGGER.debug('--> Received data %r', data)
        resp = interactors.execute_request(data, self.cache)
        self.transport.write(resp.data)


class MemcachedProtocolFactory(protocol.Factory):
    """Construct new instances of the memcached protocol"""

    def __init__(self):
        self.cache = cache.Cache()

    def buildProtocol(self, addr):
        return MemcachedProtocol(self.cache)


def serve_forever(port=9999):
    """Process incoming requests from the given socket.

    :param port: The port to listen on
    :type port: int
    """
    endpoints.serverFromString(reactor, "tcp:{}".format(port)).listen(
        MemcachedProtocolFactory()
    )
    reactor.run()
