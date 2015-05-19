# -*- coding: utf-8 -*-
"""
    pymemcache.response
    ~~~~~~~~~~~~~~~~~~~
    Interfaces for responses to commands

"""
import logging

from pymemcache import errors
from pymemcache import utils


LOGGER = logging.getLogger(__name__)


class Response(object):
    """Base class for all response objects"""

    def __init__(self, data):
        """Initialize response with data to be sent"""
        self.data = data

    def send_via(self, socket):
        """Send this response over the given socket.

        :param socket: A socket connection
        :type socket: socket.socket
        """
        if not self.data:
            raise errors.ResponseError(
                'Invalid response data. May indicate sending object of type '
                'Response or SimpleResponse instead of subclass.')

        utils.spit_connection(socket, self.data.encode('utf-8'))


class SimpleResponse(Response):
    """Base class for all simple textual responses"""

    # Sub-classes set this to the text this response transmits
    RESPONSE_BODY = None

    def __init__(self):
        super(SimpleResponse, self).__init__(self.RESPONSE_BODY)


class StoredResponse(SimpleResponse):
    """Given data was successfully stored"""
    RESPONSE_BODY = 'STORED\r\n'


class NotStoredResponse(SimpleResponse):
    """Given data was not stored"""
    RESPONSE_BODY = 'NOT_STORED\r\n'


class ExistsResponse(SimpleResponse):
    """A key exists"""
    RESPONSE_BODY = 'EXISTS\r\n'


class NotFoundResponse(SimpleResponse):
    """Key was not found"""
    RESPONSE_BODY = 'NOT_FOUND\r\n'


class GetResponse(Response):
    """Represents a get response containing key and value results"""

    def __init__(self, data):
        """Initialize this response

        :param data: Association of key to result data
        :type data: dict
        """
        if not data:
            raise errors.ResponseError('Empty response data given')

        stringified_result = ''
        for key, value in data.items():
            stringified_result += 'VALUE {} {}\r\n'.format(key, len(value))
            stringified_result += '{}\r\n'.format(value)
        stringified_result += 'END\r\n'
        super(GetResponse, self).__init__(stringified_result)
