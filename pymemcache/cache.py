# -*- coding: utf-8 -*-
"""
    pymemcache.cache
    ~~~~~~~~~~~~~~~~
    Interfaces to the in-memory cache

"""
import datetime
import logging


LOGGER = logging.getLogger(__name__)


class Cache(object):
    """Interface representing an in-memory cache"""

    def __init__(self, initial_cache=None):
        """Initialize the cache.

        :param initial_cache: The initial cache
        :type initial_cache: dict
        """
        self._cache = initial_cache or {}
        self._last_used_time = {}

    def __len__(self):
        """Return the number of items in the cache.

        :rtype: int
        """
        return len(self._cache)

    def touch(self, key):
        """Updates the last used timestamp for the given key.

        :param key: The key
        :type key: str or unicode
        """
        self._last_used_time[key] = datetime.datetime.utcnow()

    def set(self, key, value):
        """Set the key to the associated value.

        :param key: The key
        :type key: str or unicode
        :param value: The value
        :type value: str or unicode
        """
        LOGGER.debug('Inserting %r', key)
        self._cache[key] = value
        self.touch(key)

    def get(self, key):
        """Return the internal value associated with the given key.

        :param key: The key
        :type key: str or unicode
        :return: The value associated with the key or None if not found.
        :rtype: str or unicode or None
        """
        LOGGER.debug('Retrieving %r <<-FROM->> %r', key, self._cache)
        result = self._cache.get(key)
        if result:
            self.touch(key)
        return result

    def get_last_used_timestamp(self, key):
        """Return the last used timestamp for the given key.

        :param key: A key
        :type key: str or unicode
        :return: The last used timestamp for the give key or None if not
            available.
        :rtype: datetime.datetime or None
        """
        return self._last_used_time.get(key)
