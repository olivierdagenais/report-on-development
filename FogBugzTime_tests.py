"""
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
from datetime import datetime
from BeautifulSoup import BeautifulSoup, CData
import unittest
import FogBugzTime

class TestGlobalFunctions(unittest.TestCase):

    def testasIso8601zDateString(self):
        self.assertEquals("2010-02-15T00:00:00Z", FogBugzTime.asIso8601zDateString(datetime(2010, 02, 15)))
        self.assertEquals("2010-02-15T23:48:37Z", FogBugzTime.asIso8601zDateString(datetime(2010, 02, 15, 23, 48, 37)))

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
        fbt = FogBugzTime.FogBugzTime(datetime(2010, 03, 20), "", "", "")
        soup = BeautifulSoup(xml)
        resp = soup.response
        fbt.resp = resp
        fbt.interpretData()
        actual = fbt.recentActivity
        self.assertTrue("2010/02/25" in actual)
        self.assertTrue("2010/02/26" in actual)
        self.assertEquals(6.5577777777777779, actual["2010/02/27"])
        self.assertTrue("2010/02/28" in actual)
        self.assertTrue("2010/03/20" in actual)

if __name__ == '__main__':
    unittest.main()
