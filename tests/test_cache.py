# -*- coding: utf-8 -*-
import unittest

from tests import base

from pymemcache import cache


class BaseCacheTestCase(base.BaseTestCase):

    def setUp(self):
        super(BaseCacheTestCase, self).setUp()
        self.cache = cache.Cache()


class TestCacheStorage(BaseCacheTestCase):

    def test_should_start_empty(self):
        """The cache should start out empty"""
        self.assertEqual(0, len(self.cache))

    def test_should_contain_one_item_after_insertion(self):
        """Should contain one item after insertion"""
        self.cache.set('test', '1')
        self.assertEqual(1, len(self.cache))

    def test_should_return_value_after_setting_it(self):
        """Should return value after settings it"""
        self.cache.set('test', '1')
        self.assertEqual('1', self.cache.get('test'))

    def test_should_return_none_if_item_not_in_cache(self):
        """Should return None if item not in cache"""
        self.cache.set('test', '1')
        self.assertIsNone(self.cache.get('baz'))


class TestCacheTimestamps(BaseCacheTestCase):

    def test_should_update_last_used_timestamp_when_item_set(self):
        """Should update last used timestamp when item set"""
        self.cache.set('test', '1')
        prev_ts = self.cache.get_last_used_timestamp('test')
        self.cache.set('test', '2')
        self.assertNotEqual(
            prev_ts, self.cache.get_last_used_timestamp('test'))

    def test_should_update_last_used_timestamp_when_item_get(self):
        """Should update last used timestamp when item get"""
        self.cache.set('test', '1')
        prev_ts = self.cache.get_last_used_timestamp('test')
        self.cache.get('test')
        self.assertNotEqual(
            prev_ts, self.cache.get_last_used_timestamp('test'))

    def test_should_not_update_timestamp_when_getting_missing_item(self):
        """Should not update timestamp when retrieving missing item"""
        self.cache.get('test')
        self.assertIsNone(self.cache.get_last_used_timestamp('test'))

    def test_should_return_none_if_item_not_in_cache(self):
        """Should return None if item not in cache"""
        self.cache.set('test', '1')
        self.assertIsNone(self.cache.get_last_used_timestamp('baz'))


if __name__ == '__main__':
    unittest.main()
