# -*- coding: utf-8 -*-
import unittest

from tests import base
from pymemcache import request


class FromStringTest(base.BaseTestCase):

    def setUp(self):
        super(FromStringTest, self).setUp()
        self.REQUEST_FIXTURE = (
            "set herp 0 0 4\r\n")

    def test_should_raise_error_on_none(self):
        """Should raise error when None given"""
        with self.assertRaises(request.InvalidRequestError):
            request.MemcachedRequest.from_string(None)

    def test_should_raise_error_if_empty_string_given(self):
        """Should raise error if empty string given"""
        with self.assertRaises(request.InvalidRequestError):
            request.MemcachedRequest.from_string('')


if __name__ == '__main__':
    unittest.main()
