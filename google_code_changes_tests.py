import collections
from datetime import datetime
from BeautifulSoup import BeautifulSoup, CData
import unittest
import google_code_changes

class TestGlobalFunctions(unittest.TestCase):
    def test_hesc(self):
        self.assertEquals("", google_code_changes._hesc(""))
        self.assertEquals("nothing special", google_code_changes._hesc("nothing special"))
        self.assertEquals("&lt;element attributeName=&quot;attribute&#39;s value&quot; /&gt;",
                          google_code_changes._hesc("<element attributeName=\"attribute's value\" />"))

    def testbeginningOfDay(self):
        actual = google_code_changes.beginningOfDay(datetime(2010, 03, 19, 22, 21, 42))
        self.assertEquals(2010, actual.year)
        self.assertEquals(03, actual.month)
        self.assertEquals(19, actual.day)
        self.assertEquals(00, actual.hour)
        self.assertEquals(00, actual.minute)
        self.assertEquals(00, actual.second)

    def testnextDay(self):
        actual = google_code_changes.nextDay(datetime(2010, 03, 19, 22, 21, 42))
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
        actual = google_code_changes.convertActivityDictionaryToValueArray(activity, marchFirst, datetime(2010,03,14))
        self.assertEquals([1, 2, 3, 0, 5, 0, 0, 8, 0, 0, 0, 0, 13, 0], actual)

    def testresponseTypical(self):
        xml = """<?xml version="1.0"?>
<feed>
    <entry><updated>2009-12-05T03:13:15Z</updated></entry>
    <entry><updated>2009-12-04T15:54:38Z</updated></entry>
    <entry><updated>2009-11-25T22:56:03Z</updated></entry>
    <entry><updated>2009-11-22T20:18:28Z</updated></entry>
</feed>
"""
        soup = BeautifulSoup(xml)
        actual = google_code_changes.response(soup, datetime(2009, 12, 05))
        self.assertEquals("<img src='http://chart.apis.google.com/chart?chof=png&chco=00FF00&chd=s:9AA9AAAAAAAA99"
                          + "&chds=0,1&chm=B,d0efd0,0,0,0&chma=30,15&chs=450x150&cht=lc&chxl=2:|today|2009/11/22"
                          + "&chxp=2,0,13&chxr=0,13,0|1,0,1,1|2,13,0"
                          + "&chxs=0,000000,10,0,t|1,000000,10,1,lt|2,000000,10,0&chxt=x,y,x' />", actual)

    def testresponseWithSingleDigitMonthAndDay(self):
        xml = """<?xml version="1.0"?>
<feed>
    <entry><updated>2010-01-02T03:13:15Z</updated></entry>
    <entry><updated>2010-01-01T15:54:38</updated></entry>
</feed>
"""
        soup = BeautifulSoup(xml)
        actual = google_code_changes.response(soup, datetime(2010, 01, 02))
        self.assertEquals("<img src='http://chart.apis.google.com/chart?chof=png&chco=00FF00&chd=s:99"
                          + "&chds=0,1&chm=B,d0efd0,0,0,0&chma=30,15&chs=450x150&cht=lc&chxl=2:|today|2010/01/01"
                          + "&chxp=2,0,1&chxr=0,1,0|1,0,1,1|2,1,0"
                          + "&chxs=0,000000,10,0,t|1,000000,10,1,lt|2,000000,10,0&chxt=x,y,x' />", actual)

if __name__ == '__main__':
    unittest.main()
