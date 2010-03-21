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
from datetime import datetime, timedelta
from dateutil import parser as dateParser
import urllib
import urllib2
import collections
from BeautifulSoup import BeautifulSoup, CData
from Chart import Chart

feedUrlTemplate = "http://code.google.com/feeds/p/%PROJECT%/svnchanges/basic?path=%PATH%";
entries = 50;

def _hesc(str):
    # '<' and '>'
    str = str.replace("<", "&lt;").replace(">", "&gt;")
    # '"' and '
    str = str.replace('"', "&quot;").replace("'", "&#39;")

    return str

def getFeed(projectName, projectPath):
    opener = urllib2.build_opener()
    feedUrl = feedUrlTemplate.replace("%PROJECT%", _hesc(projectName)).replace("%PATH%", _hesc(projectPath))
    resp = BeautifulSoup(opener.open(feedUrl))
    return resp

def beginningOfDay(date):
    return datetime(date.year, date.month, date.day)

def nextDay(date):
    return date + timedelta(days = 1)

def response(obj, lastDay):
    feed = obj.first()

    chart = Chart()
    chart.cht = "lc"
    chart.chs = "450x150" # TODO: parameterize
    chart.chma = "30,15"  # TODO: determine if that will be enough room

    chart.chco = "00FF00"
    chart.chm = "B,d0efd0,0,0,0"
    chart.chxt = "x,y,x"
    chart.chxs = "0,000000,10,0,t" + "|1,000000,10,1,lt" + "|2,000000,10,0"

    commitsByDay = collections.defaultdict(int)
    lastDay = beginningOfDay(lastDay)
    earliestDay = nextDay(lastDay)
    for entry in feed.findAll('entry'):
        date = dateParser.parse(entry.updated.text)
        dayKey = beginningOfDay(date)
        if dayKey < earliestDay:
            earliestDay = dayKey

        commitsByDay[dayKey] += 1

    currentDay = earliestDay
    values = [ ]
    while currentDay <= lastDay:
        if currentDay in commitsByDay:
            values.append(commitsByDay[currentDay])
        else:
            values.append(0)
        currentDay = nextDay(currentDay)

    chart.addData(values)

    chart.chxl = "2:|today|" + str(date.year) + "/" + str(date.month) + "/" + str(date.day)
    chart.chxp = "2,0," + str(len(values) - 1)

    html = chart.asImgElement()
    return html

if __name__ == "__main__":
    projectName = sys.argv[1];
    projectPath = sys.argv[2];
    resp = getFeed(projectName, projectPath)
    print(response(resp, datetime.utcnow()))
