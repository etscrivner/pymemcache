# -*- coding: utf-8 -*-
"""
    pymemcache.errors
    ~~~~~~~~~~~~~~~~~
    Exceptions base classes for pymemcache

"""


class Error(Exception):
    """Base exception for all pymemcache errors"""


class ConnectionError(Error):
    """Base class for any socket-level connection issues"""


class RequestError(Error):
    """Base class for errors related to the request contents"""
