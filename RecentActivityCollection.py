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

def configureChart(chart):
    chart.cht = "lc"
    chart.chma = "30,15"  # TODO: determine if that will be enough room

    chart.chco = "00FF00"
    chart.chm = "B,d0efd0,0,0,0"
    chart.chxt = "x,y,x"
    chart.chxs = "0,000000,10,0,t" + "|1,000000,10,1,lt" + "|2,000000,10,0"

def renderMetadata(chart, earliestDay, maxValueCount):
    chart.chxl = "2:|today|" + earliestDay.strftime("%Y/%m/%d")
    chart.chxp = "2,0," + str(maxValueCount - 1)

class RecentActivityCollection:
    def __init__(self, width, height):
        self.recentActivities = [ ]
        self.chart = Chart()
        self.chart.chs = "%dx%d" % (width, height)
        configureChart(self.chart)

    def append(self, recentActivity):
        self.recentActivities.append(recentActivity)

    def renderChart(self):
        first = self.recentActivities[0]
        earliestDay = first.getEarliestDay()
        values = first.convertToValueArray()
        self.chart.addData(values)
        maxValueCount = len(values)
        for ra in self.recentActivities[1:]:
            earliestDay = min(earliestDay, ra.getEarliestDay())
            values = ra.convertToValueArray()
            self.chart.addData(values)
            maxValueCount = max(maxValueCount, len(values))

        renderMetadata(self.chart, earliestDay, maxValueCount)
        return self.chart

if __name__ == "__main__":
    rac = RecentActivityCollection(int(sys.argv[1]), int(sys.argv[2]))
    ra = RecentActivity(sys.argv[3])
    for arg in sys.argv[4:]:
        (name, value) = string.split(arg, '=')
        ra[name] = value
    rac.append(ra)
    c = rac.renderChart()
    print(c.str())
