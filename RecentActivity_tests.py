import collections
from datetime import datetime
import unittest
import RecentActivity

class TestGlobalFunctions(unittest.TestCase):

    def testasDateKey(self):
        actual = RecentActivity.asDateKey("2010/03/19T22:21:42Z")
        self.assertEquals(2010, actual.year)
        self.assertEquals(03, actual.month)
        self.assertEquals(19, actual.day)
        self.assertEquals(00, actual.hour)
        self.assertEquals(00, actual.minute)
        self.assertEquals(00, actual.second)

    def testbeginningOfDay(self):
        actual = RecentActivity.beginningOfDay(datetime(2010, 03, 19, 22, 21, 42))
        self.assertEquals(2010, actual.year)
        self.assertEquals(03, actual.month)
        self.assertEquals(19, actual.day)
        self.assertEquals(00, actual.hour)
        self.assertEquals(00, actual.minute)
        self.assertEquals(00, actual.second)

    def testnextDay(self):
        actual = RecentActivity.nextDay(datetime(2010, 03, 19, 22, 21, 42))
        self.assertEquals(2010, actual.year)
        self.assertEquals(03, actual.month)
        self.assertEquals(20, actual.day)
        self.assertEquals(22, actual.hour)
        self.assertEquals(21, actual.minute)
        self.assertEquals(42, actual.second)

    def testconvertActivityDictionaryToValueArray(self):
        activity = collections.defaultdict(int)
        marchFirst = datetime(2010,03,01)
        activity[marchFirst] = 1
        activity[datetime(2010,03,02)] = 2
        activity[datetime(2010,03,03)] = 3
        activity[datetime(2010,03,05)] = 5
        activity[datetime(2010,03, 8)] = 8
        activity[datetime(2010,03,13)] = 13
        actualEarliestDay, actualValues = RecentActivity.convertActivityDictionaryToValueArray(activity, datetime(2010,03,14))
        self.assertEquals(marchFirst, actualEarliestDay)
        self.assertEquals([1, 2, 3, 0, 5, 0, 0, 8, 0, 0, 0, 0, 13, 0], actualValues)

    def testcreateChartHelperMethod(self):
        actual = RecentActivity.createChart([1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], datetime(2009, 11, 22))
        self.assertEquals("s:9AA9AAAAAAAA99", actual.chd)
        self.assertEquals("2:|today|2009/11/22", actual.chxl)
        self.assertEquals("2,0,13", actual.chxp)

    def testcreateChartInstanceMethod(self):
        ra = RecentActivity.RecentActivity("2009/12/05")
        ra["2009-12-05T03:13:15Z"] = 1
        ra["2009-12-04T15:54:38Z"] = 1
        ra["2009-11-25T22:56:03Z"] = 1
        ra["2009-11-22T20:18:28Z"] = 1
        actual = ra.createChart()
        self.assertEquals("s:9AA9AAAAAAAA99", actual.chd)
        self.assertEquals("2:|today|2009/11/22", actual.chxl)
        self.assertEquals("2,0,13", actual.chxp)

    def testcreateChartWithSingleDigitMonthAndDay(self):
        actual = RecentActivity.createChart([1, 1], datetime(2010, 01, 01))
        self.assertEquals("s:99", actual.chd)
        self.assertEquals("2:|today|2010/01/01", actual.chxl)
        self.assertEquals("2,0,1", actual.chxp)

if __name__ == '__main__':
    unittest.main()
