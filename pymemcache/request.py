# -*- coding: utf-8 -*-
"""
    pymemcache.request
    ~~~~~~~~~~~~~~~~~~
    Facilities for representing and processing requests.

"""
import logging

from pymemcache import errors


LOGGER = logging.getLogger(__name__)


class InvalidRequestError(errors.Error):
    """Error raised when a request is malformed or invalid"""


def parse_command(raw_data):
    """Parse the command-line and body from raw string data.

    :param raw_data: The raw string data
    :type raw_data: str or unicode
    :return: (str, [str])
    :rtype: tuple
    """
    if not raw_data:
        raise InvalidRequestError('Request contains no data.')

    parts = [each.strip() for each in raw_data.split('\r\n') if each.strip()]

    if not parts:
        raise InvalidRequestError('Could not parse request.')

    return (parts.pop(0), parts)


def is_valid_command(command):
    """Indicates whether or not the given command is valid.

    :param command: A command
    :type command: str or unicode
    :rtype: bool
    """
    # TODO(etscrivner): Eventually we'd like to construct this dynamically from
    # a list of all available commands
    valid_commands = [
        'add', 'append', 'decr', 'delete', 'flush_all', 'get', 'gets', 'incr',
        'prepend', 'quit', 'replace', 'set', 'stats', 'verbosity', 'version',
    ]

    if not command:
        return False

    parts = command.split('\r\n')
    command_parts = parts[0].split(' ')

    command = command_parts[0]
    return command.strip().lower() in valid_commands
