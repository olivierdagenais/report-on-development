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

    def testaddDataSimple(self):
        c = google_code_changes.Chart()
        google_code_changes.addData(c, [12, 40, 39, 36, 30, 50, 44])
        self.assertEquals("0,50", c.chds)
        self.assertEquals("0,6,0|1,0,50,1|2,6,0", c.chxr)
        self.assertEquals("s:Pxwsl92", c.chd)

    def testaddDataExtended(self):
        c = google_code_changes.Chart()
        google_code_changes.addData(c, [808, 2532, 1970, 2879])
        self.assertEquals("0,2879", c.chds)
        self.assertEquals("0,3,0|1,0,2879,1|2,3,0", c.chxr)
        self.assertEquals("e:R94Rry..", c.chd)

    def testserializeChartEmpty(self):
        c = google_code_changes.Chart()
        c.name = "value"
        self.assertEquals("chof=png&name=value", google_code_changes.serializeChart(c))

    def testserializeChartOnePair(self):
        c = google_code_changes.Chart()
        c.name = "value"
        self.assertEquals("chof=png&name=value", google_code_changes.serializeChart(c))

    def testserializeChartWithValue(self):
        c = google_code_changes.Chart()
        google_code_changes.addData(c, [42])
        self.assertEquals("chof=png&chd=s:9&chds=0,42&chxr=0,0,0|1,0,42,1|2,0,0", google_code_changes.serializeChart(c))

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

    def testresponse(self):
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

if __name__ == '__main__':
    unittest.main()
