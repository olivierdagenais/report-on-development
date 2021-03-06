﻿"""
Copyright 2010 Olivier Dagenais

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
import chart_encoding

class TestGlobalFunctions(unittest.TestCase):

    def testis_number(self):
        self.assertTrue(chart_encoding.is_number("1"))
        self.assertTrue(chart_encoding.is_number("0"))
        self.assertTrue(chart_encoding.is_number("-1"))

        self.assertFalse(chart_encoding.is_number(""))
        self.assertFalse(chart_encoding.is_number("a"))
        self.assertFalse(chart_encoding.is_number("4a"))

    def testsimpleEncode(self):
        self.assertEqual("", chart_encoding.simpleEncode([], 61))
        self.assertEqual("ABZabz09", chart_encoding.simpleEncode([0, 1, 25, 26, 27, 51, 52, 61], 61))
        self.assertEqual("Monkeys", chart_encoding.simpleEncode([12, 40, 39, 36, 30, 50, 44], 61))
        self.assertEqual("_9_", chart_encoding.simpleEncode([-1, 61, 62], 61))

    def testsimpleEncodeRoundingError(self):
        self.assertEqual("AF49", chart_encoding.simpleEncode([0, 1, 11, 12], 12))

    def testextendedEncode(self):
        self.assertEqual("", chart_encoding.extendedEncode([], 4095))
        self.assertEqual("Monkeys.", chart_encoding.extendedEncode([808, 2532, 1970, 2879], 4095))
        self.assertEqual("AAABAZAaAbAz.-..", chart_encoding.extendedEncode([0, 1, 25, 26, 27, 51, 4094, 4095], 4095))
        self.assertEqual("__..__", chart_encoding.extendedEncode([-1, 4095, 4096], 4095))

    def testextendedEncodeRoundingError(self):
        self.assertEqual("AAAB.-..", chart_encoding.extendedEncode([0, 1, 2878, 2879], 2879))

if __name__ == '__main__':
    unittest.main()
