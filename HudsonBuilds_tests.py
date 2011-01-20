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
import HudsonBuilds

class TestGlobalFunctions(unittest.TestCase):

    def testInjectedFeedXml(self):
        xml = """<?xml version="1.0"?>
<feed>
    <entry><title>#35 (SUCCESS)</title><updated>2010-04-04T18:12:26Z</updated></entry>
    <entry><title>#34 (FAILURE)</title><updated>2010-04-04T14:29:06Z</updated></entry>
    <entry><title>#33 (stable)</title><updated>2010-04-03T20:57:35Z</updated></entry>
    <entry><title>#32 (FAILURE)</title><updated>2010-04-03T18:18:21Z</updated></entry>
    <entry><title>#31 (back to normal)</title><updated>2010-04-03T12:54:35Z</updated></entry>
    <entry><title>#30 (SUCCESS)</title><updated>2010-04-02T12:42:07Z</updated></entry>
    <entry><title>#29 (SUCCESS)</title><updated>2010-03-27T15:46:07Z</updated></entry>
    <entry><title>#28 (SUCCESS)</title><updated>2010-03-03T03:21:28Z</updated></entry>
    <entry><title>#27 (SUCCESS)</title><updated>2009-12-04T15:56:36Z</updated></entry>
    <entry><title>#26 (SUCCESS)</title><updated>2009-11-22T23:01:37Z</updated></entry>
</feed>
"""
        hb = HudsonBuilds.HudsonBuilds(datetime(2010, 04, 06), "hudsonUrl", "jobName")
        hb.feedXml = BeautifulSoup(xml)
        hb.interpretData()
        chart = hb.renderChart(450, 150)
        chart.processData()
        self.assertEquals("s:"+
                            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + 
                            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
                            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
                            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
                            "AAAAffAA" +
                            "," +
                            "fAAAAAAAAAAAfAAAAAAAAAAAAAAAAAAA" +
                            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
                            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" +
                            "AAAAAfAAAAAAAAAAAAAAAAAAAAAAAfAA" +
                            "AAAf9fAA", chart.chd)

if __name__ == '__main__':
    unittest.main()
