#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Simple service to make links short '''

import hashlib
import unittest


def shorter(long_URL):
    if long_URL:
        key = hashlib.md5(long_URL.encode())
        return key.hexdigest()
    else:
        return None


class TestShortlnk(unittest.TestCase):

    def test_shorter(self):
        test_str1 = "https://www.google.ru/search?q=hashlib.md5+python&newwindow=1&safe=strict&ei=SXyTW4WCJIqosAH0v6TACw&start=10&sa=N&biw=1301&bih=629"
        self.assertTrue(shorter(test_str1))
        test_str2=''
        self.assertFalse(shorter(test_str2))


