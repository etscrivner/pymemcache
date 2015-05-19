# -*- coding: utf-8 -*-
"""
    pymemcache.interactors
    ~~~~~~~~~~~~~~~~~~~~~~
    Interfaces for ingesting requests and returning responses.

"""
import logging

from pymemcache import request
from pymemcache import response


LOGGER = logging.getLogger(__name__)


def execute_request(raw_data, the_cache):
    """Parse and execute the given request, returning a response.

    :param raw_data: The raw request data
    :type raw_data: str or unicode
    :param the_cache: The in-memory cache for this process
    :type the_cache: mixed
    """
    command, body = request.parse_command(raw_data)
    LOGGER.debug('--> Command %r', command)

    if command.startswith('get'):
        key = command.split(' ')[1]
        result = the_cache.get(key)
        if not result:
            return response.NotFoundResponse()
        return response.GetResponse({key: result})

    if command.startswith('set'):
        key = command.split(' ')[1]
        the_cache.set(key, body[0])
        return response.StoredResponse()
