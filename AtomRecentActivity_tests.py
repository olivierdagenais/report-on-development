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
import AtomRecentActivity

class TestGlobalFunctions(unittest.TestCase):

    def testInjectedFeedXml(self):
        xml = """<?xml version="1.0"?>
<feed>
    <entry><updated>2009-12-05T03:13:15Z</updated></entry>
    <entry><updated>2009-12-04T15:54:38Z</updated></entry>
    <entry><updated>2009-11-25T22:56:03Z</updated></entry>
    <entry><updated>2009-11-22T20:18:28Z</updated></entry>
</feed>
"""
        ara = AtomRecentActivity.AtomRecentActivity("", datetime(2009, 12, 05))
        ara.feedXml = BeautifulSoup(xml)
        ara.interpretFeed()
        actual = ara.createChartHtml()
        self.assertEquals("<img src='http://chart.apis.google.com/chart?chof=png&chco=00FF00&chd=s:9AA9AAAAAAAA99"
                          + "&chds=0,1.0&chm=B,d0efd0,0,0,0&chma=30,15&chs=450x150&cht=lc&chxl=2:|today|2009/11/22"
                          + "&chxp=2,0,13&chxr=0,13,0,1|1,0,1.0,1|2,13,0"
                          + "&chxs=0,000000,10,0,t|1,000000,10,1,lt|2,000000,10,0&chxt=x,y,x'"
                          + " width='450' height='150' />", actual)

if __name__ == '__main__':
    unittest.main()
