# -*- coding: utf-8 -*-
"""
    pymemcache.request
    ~~~~~~~~~~~~~~~~~~
    Facilities for representing and processing requests.

"""
import logging

from pymemcache import errors


logger = logging.getLogger(__name__)


class InvalidRequestError(errors.Error):
    """Error raised when a request is malformed or invalid"""


def is_valid_request(command):
    """Indicates whether or not the given command is valid.

    :param command: A command
    :type command: str or unicode
    :rtype: bool
    """
    if not command:
        return False

    parts = command.split('\r\n')
    return 'get' in parts[0].lower()
