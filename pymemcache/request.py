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
