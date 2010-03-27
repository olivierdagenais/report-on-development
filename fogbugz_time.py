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
from fogbugz import FogBugz
from datetime import datetime, timedelta
from dateutil import parser as dateParser
from RecentActivity import RecentActivity
from RecentActivityCollection import RecentActivityCollection

def getData(fogBugzUrl, userName, password, today):
    oneMonthAgo = today - timedelta(days = 28)
    fb = FogBugz(fogBugzUrl)
    fb.logon(userName, password)
    resp = fb.listIntervals(dtStart=asIso8601zDateString(oneMonthAgo), dtEnd=asIso8601zDateString(today))
    return resp

"""
Formats a datetime object into a string like:
2010-02-15T00:00:00Z
"""
def asIso8601zDateString(date):
    result = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return result

def response(resp, lastDay):
    ra = RecentActivity(lastDay)
    for interval in resp.intervals.findAll('interval'):
        if interval.fdeleted.text != 'false': continue
        dtStart = dateParser.parse(interval.dtstart.text)
        dtEnd = dateParser.parse(interval.dtend.text)
        interval = dtEnd - dtStart
        ra[dtStart] += interval.seconds

    return ra

if __name__ == "__main__":
    today = dateParser.parse(sys.argv[1])
    resp = getData(sys.argv[2], sys.argv[3], sys.argv[4], today)
    ra = response(resp, today)
    rac = RecentActivityCollection(450, 150)
    rac.append(ra)
    chart = rac.renderChart()
    print(chart.asImgElement())
