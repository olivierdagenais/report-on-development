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
import collections
from datetime import datetime
import unittest
import Chart
import RecentActivityCollection
import RecentActivity

class TestGlobalFunctions(unittest.TestCase):

    def testrenderChartDataSimple(self):
        lastDay = "2009/12/05"
        rac = RecentActivityCollection.RecentActivityCollection(lastDay)
        ra = RecentActivity.RecentActivity(lastDay)
        ra["2009-12-05T03:13:15Z"] = 1
        ra["2009-12-04T15:54:38Z"] = 1
        ra["2009-11-25T22:56:03Z"] = 1
        ra["2009-11-22T20:18:28Z"] = 1
        rac.append(ra)
        c = Chart.Chart()
        c.chs = "450x150"
        actualEarliestDay, actualMaxValueCount = rac.renderChartData(c)
        c.processData()
        self.assertEquals("s:9AA9AAAAAAAA99", c.chd)
        self.assertEquals(datetime(2009,11,22), actualEarliestDay)
        self.assertEquals(14, actualMaxValueCount)

    def testrenderChartDataTwoSetsWithDisconnectedData(self):
        lastDay = "2010/04/06"
        rac = RecentActivityCollection.RecentActivityCollection(lastDay)
        firstRa = RecentActivity.RecentActivity(lastDay)
        firstRa["2010-04-04T18:12:26Z"] = 1
        firstRa["2009-11-22T23:01:37Z"] = 1
        rac.append(firstRa)

        secondRa = RecentActivity.RecentActivity(lastDay)
        secondRa["2010-04-04T18:12:26Z"] = 1
        secondRa["2010-04-03T18:18:21Z"] = 1
        rac.append(secondRa)

        c = Chart.Chart()
        c.chs = "450x150"
        actualEarliestDay, actualMaxValueCount = rac.renderChartData(c)
        self.assertEquals(datetime(2009,11,22), actualEarliestDay)
        self.assertEquals(136, len(c.dataSets[0]))
        self.assertEquals(136, len(c.dataSets[1]))

if __name__ == '__main__':
    unittest.main()
