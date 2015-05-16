# -*- coding: utf-8 -*-
import unittest

from tests import base
from pymemcache import request


class TestIsValidRequest(base.BaseTestCase):

    def should_return_false_for_none_request(self):
        """Should return False for none request"""
        self.assertFalse(request.is_valid_command(None))

    def test_should_return_false_for_empty_request(self):
        """Should return False for empty request"""
        self.assertFalse(request.is_valid_command(''))

    def test_should_return_true_for_single_command(self):
        """Should return true for single command"""
        self.assertTrue(request.is_valid_command('flush_all\r\n'))

    def test_should_return_true_for_multiarg_valid_command(self):
        """Should return true for get command"""
        self.assertTrue(request.is_valid_command('get test1 test2 test3\r\n'))


if __name__ == '__main__':
    unittest.main()
