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
