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
from RecentActivity import RecentActivity

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

class RecentActivitySource:
    def __init__(self, lastDay):
        self.lastDay = lastDay
        self.recentActivity = RecentActivity(lastDay)
    
    def renderChart(self, width, height):
        chart = Chart()
        chart.chs = "%dx%d" % (width, height)

        configureChart(chart)
        earliestDay, maxValueCount = self.renderChartData(chart)
        renderMetadata(chart, earliestDay, maxValueCount)

        return chart

    def collectData(self):
        raise NotImplementedError()

    def interpretData(self):
        raise NotImplementedError()

    def renderChartData(self, chart):
        earliestDay = self.recentActivity.getEarliestDay()
        values = self.recentActivity.convertToValueArray()
        chart.addData(values)
        maxValueCount = len(values)
        return earliestDay, maxValueCount

    def printTestChartHtml(self):
        self.collectData()
        self.interpretData()
        chart = self.renderChart(450, 150)
        print(chart.asImgElement())
