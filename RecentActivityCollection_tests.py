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
import collections
from datetime import datetime
import unittest
import Chart
import RecentActivityCollection
import RecentActivity

class TestGlobalFunctions(unittest.TestCase):

    def testrenderChart(self):
        rac = RecentActivityCollection.RecentActivityCollection(450, 150)
        ra = RecentActivity.RecentActivity("2009/12/05")
        ra["2009-12-05T03:13:15Z"] = 1
        ra["2009-12-04T15:54:38Z"] = 1
        ra["2009-11-25T22:56:03Z"] = 1
        ra["2009-11-22T20:18:28Z"] = 1
        rac.append(ra)
        actual = rac.renderChart()
        actual.processData()
        self.assertEquals("s:9AA9AAAAAAAA99", actual.chd)
        self.assertEquals("2:|today|2009/11/22", actual.chxl)
        self.assertEquals("2,0,13", actual.chxp)

    def testrenderMetadata(self):
        c = Chart.Chart()
        RecentActivityCollection.renderMetadata(c, datetime(2010, 01, 01), 2)
        self.assertEquals("2:|today|2010/01/01", c.chxl)
        self.assertEquals("2,0,1", c.chxp)

if __name__ == '__main__':
    unittest.main()
