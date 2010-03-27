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
import string
import sys
from Chart import Chart
from RecentActivitySource import RecentActivitySource

class RecentActivityCollection(RecentActivitySource):
    def __init__(self, lastDay):
        self.recentActivities = [ ]
        RecentActivitySource.__init__(self, lastDay)

    # TODO: could also add create() method that creates RecentActivity instances (with our lastDay) and appends them 
    def append(self, recentActivity):
        self.recentActivities.append(recentActivity)

    def collectData(self):
        pass

    def interpretData(self):
        pass

    def renderChartData(self, chart):
        first = self.recentActivities[0]
        earliestDay = first.getEarliestDay()
        values = first.convertToValueArray()
        chart.addData(values)
        maxValueCount = len(values)
        for ra in self.recentActivities[1:]:
            earliestDay = min(earliestDay, ra.getEarliestDay())
            values = ra.convertToValueArray()
            chart.addData(values)
            maxValueCount = max(maxValueCount, len(values))

        return (earliestDay, maxValueCount)
