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
        self.assertEqual("s:", chart_encoding.simpleEncode([], 61))
        self.assertEqual("s:ABZabz09", chart_encoding.simpleEncode([0, 1, 25, 26, 27, 51, 52, 61], 61))
        self.assertEqual("s:Monkeys", chart_encoding.simpleEncode([12, 40, 39, 36, 30, 50, 44], 61))
        self.assertEqual("s:_9_", chart_encoding.simpleEncode([-1, 61, 62], 61))

    def testsimpleEncodeRoundingError(self):
        self.assertEqual("s:AF49", chart_encoding.simpleEncode([0, 1, 11, 12], 12))

    def testextendedEncode(self):
        self.assertEqual("e:", chart_encoding.extendedEncode([], 4095))
        self.assertEqual("e:Monkeys.", chart_encoding.extendedEncode([808, 2532, 1970, 2879], 4095))
        self.assertEqual("e:AAABAZAaAbAz.-..", chart_encoding.extendedEncode([0, 1, 25, 26, 27, 51, 4094, 4095], 4095))
        self.assertEqual("e:__..__", chart_encoding.extendedEncode([-1, 4095, 4096], 4095))

    def testextendedEncodeRoundingError(self):
        self.assertEqual("e:AAAB.-..", chart_encoding.extendedEncode([0, 1, 2878, 2879], 2879))

if __name__ == '__main__':
    unittest.main()
