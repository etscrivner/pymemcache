# -*- coding: utf-8 -*-
import collections
import unittest

from pymemcache import errors
from pymemcache import response
from tests import base


class TestGetResponse(base.BaseTestCase):

    def test_should_raise_error_if_empty_get_response(self):
        """Should raise error if empty data given to get response"""
        self.assertRaises(errors.ResponseError, response.GetResponse, {})

    def test_should_correctly_serialize_single_item_dict(self):
        """Should correctly serialized single item dict"""
        fixture = {'hello': 'you'}
        resp = response.GetResponse(fixture)
        self.assertEqual(
            "VALUE hello 3\r\nyou\r\nEND\r\n",
            resp.data
        )

    def test_should_correctly_serialize_multi_item_dict(self):
        """Should correctly serialize multi-item dict"""
        fixture = collections.OrderedDict({'hello': 'you', 'good': 'byte'})
        resp = response.GetResponse(fixture)
        self.assertEqual(
            "VALUE good 4\r\nbyte\r\nVALUE hello 3\r\nyou\r\nEND\r\n",
            resp.data
        )


if __name__ == '__main__':
    unittest.main()
