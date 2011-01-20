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
import sys
import Chart
from datetime import datetime, timedelta
from dateutil import parser as dateParser
from AtomRecentActivity import AtomRecentActivity
from RecentActivity import RecentActivity
from RecentActivityCollection import renderChartData

feedUrlTemplate = "%s/job/%s/rssAll";

class HudsonBuilds(AtomRecentActivity):
    def __init__(self, lastDay, hudsonUrl, jobName):
        feedUrl = feedUrlTemplate % (hudsonUrl, jobName)
        AtomRecentActivity.__init__(self, lastDay, feedUrl)
        self.successes = RecentActivity(lastDay)
        self.failures = RecentActivity(lastDay)

    def logEntryAsActivity(self, entry):
        ra = self.successes if self.representsSuccess(entry.title.text) else self.failures
        ra[entry.updated.text] += 1

    def representsSuccess(self, titleText):
        return (" (SUCCESS)" in titleText) or (" (stable)" in titleText) or (" (back to normal)" in titleText)

    def renderChartData(self, chart):
        earliestDay, maxValueCount = renderChartData([self.failures, self.successes], chart)
        chart.chco = "FF0000,00FF00"
        width, height = chart.getEffectiveDimensions()
        numPixelsPerDay = width / maxValueCount
        if numPixelsPerDay > Chart.minPixelsBetweenHorizontalAxisValues:
            # small enough number of values for a bar chart with stacked values
            chart.cht = "bvs"
            chart.chm = ""
            chart.chbh = "a"
        return (earliestDay, maxValueCount)

if __name__ == "__main__":
    hb = HudsonBuilds(datetime.utcnow(), sys.argv[1], sys.argv[2])
    hb.printTestChartHtml()
