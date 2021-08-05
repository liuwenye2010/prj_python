#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" py  unittest """ 
""" py_unittest.py  -v """
"""python -m unittest -v  py_unittest.py """


import sys
import unittest


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        print ("=>setUp")

    def tearDown(self):
        print ("<=tearDown")

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(sys.version_info[0] < 4,
                     "not supported in python version < 3")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_windows_support(self):
        # windows specific testing code
        pass

    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "broken")

if __name__ == '__main__':
    unittest.main()