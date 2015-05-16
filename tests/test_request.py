# -*- coding: utf-8 -*-
import unittest

from tests import base
from pymemcache import request


class TestParseCommand(base.BaseTestCase):

    def test_should_raise_error_if_none_given(self):
        """Should raise error if None given"""
        self.assertRaises(
            request.InvalidRequestError, request.parse_command, None)

    def test_should_raise_error_if_empty_string_given(self):
        """Should raise error if empty string given"""
        self.assertRaises(
            request.InvalidRequestError, request.parse_command, '')

    def test_should_raise_error_if_contains_only_space_characters(self):
        """Should raise error if only space characters given"""
        self.assertRaises(
            request.InvalidRequestError,
            request.parse_command, '\r\n\t\r\n \r\n')

    def test_should_return_correct_parts_for_a_lone_command(self):
        """Should return the correct parts for a lone command"""
        command_line, body = request.parse_command('get test\r\n')
        self.assertEqual(command_line, 'get test')
        self.assertEqual([], body)

    def test_should_return_correct_parts_for_multiline_command(self):
        """Should return correct parts for multi-line command"""
        command_line, body = request.parse_command(
            'set test\r\nhello\r\nend'
        )
        self.assertEqual(command_line, 'set test')
        self.assertEqual(set(['hello', 'end']), set(body))


class TestIsValidRequest(base.BaseTestCase):

    def test_should_return_false_for_none_request(self):
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
