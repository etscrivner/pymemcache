# -*- coding: utf-8 -*-
import unittest

from tests import base


class TestServer(base.BaseTestCase):

    def test_should_fail(self):
        self.fail('Should write some tests for this stuff!')


if __name__ == '__main__':
    unittest.main()