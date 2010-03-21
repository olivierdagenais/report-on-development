from datetime import datetime
from BeautifulSoup import BeautifulSoup, CData
import unittest
import fogbugz_time

class TestGlobalFunctions(unittest.TestCase):

    def testasIso8601zDateString(self):
        self.assertEquals("2010-02-15T00:00:00Z", fogbugz_time.asIso8601zDateString(datetime(2010, 02, 15)))
        self.assertEquals("2010-02-15T23:48:37Z", fogbugz_time.asIso8601zDateString(datetime(2010, 02, 15, 23, 48, 37)))

    def testresponseTypical(self):
        xml = """<?xml version="1.0"?>
<response>
    <intervals>
<interval><dtStart>2010-02-25T00:49:44Z</dtStart><dtEnd>2010-02-25T01:52:39Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-02-26T19:04:00Z</dtStart><dtEnd>2010-02-26T20:30:00Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-02-27T14:01:34Z</dtStart><dtEnd>2010-02-27T17:05:17Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-02-27T18:30:00Z</dtStart><dtEnd>2010-02-27T21:59:45Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-02-28T01:00:16Z</dtStart><dtEnd>2010-02-28T02:58:45Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-03-20T16:04:30Z</dtStart><dtEnd>2010-03-20T16:41:35Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-03-20T17:14:28Z</dtStart><dtEnd>2010-03-20T17:33:41Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-03-20T18:00:11Z</dtStart><dtEnd>2010-03-20T18:39:44Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-03-20T18:52:40Z</dtStart><dtEnd>2010-03-20T19:39:17Z</dtEnd><fDeleted>false</fDeleted></interval>
<interval><dtStart>2010-03-20T19:43:15Z</dtStart><dtEnd>2010-03-20T22:07:48Z</dtEnd><fDeleted>false</fDeleted></interval>
    </intervals>
</response>
"""
        soup = BeautifulSoup(xml)
        resp = soup.response
        actual = fogbugz_time.response(resp, datetime(2010, 03, 20))
        self.assertEquals("<img src='http://chart.apis.google.com/chart?chof=png&chco=00FF00"
                          + "&chd=e:KPN...TRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAur"
                          + "&chds=0,23608.0&chm=B,d0efd0,0,0,0&chma=30,15&chs=450x150&cht=lc&chxl=2:|today|2010/02/25"
                          + "&chxp=2,0,23&chxr=0,23,0|1,0,23608.0,1|2,23,0"
                          + "&chxs=0,000000,10,0,t|1,000000,10,1,lt|2,000000,10,0&chxt=x,y,x' />", actual)

if __name__ == '__main__':
    unittest.main()
