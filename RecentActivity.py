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
from datetime import datetime, timedelta
from dateutil import parser as dateParser
import collections

def asDateKey(date):
    if isinstance(date, basestring):
        date = dateParser.parse(date)
    return beginningOfDay(date)

def beginningOfDay(date):
    return datetime(date.year, date.month, date.day)

def nextDay(date):
    return date + timedelta(days = 1)

def getEarliestDay(activityByDay, lastDay):
    earliestDay = nextDay(lastDay)
    for day in activityByDay.keys():
        if day < earliestDay:
            earliestDay = day
    return earliestDay

def convertActivityDictionaryToValueArray(activityByDay, earliestDay, lastDay):
    currentDay = earliestDay
    values = [ ]
    while currentDay <= lastDay:
        if currentDay in activityByDay:
            values.append(activityByDay[currentDay])
        else:
            values.append(0)
        currentDay = nextDay(currentDay)
    return values

class RecentActivity:
    def __init__(self, lastDay):
        self.lastDay = asDateKey(lastDay)
        self.activityByDay = collections.defaultdict(float)

    def convertToValueArray(self):
        earliestDay = self.getEarliestDay()
        values = convertActivityDictionaryToValueArray(self.activityByDay, earliestDay, self.lastDay)
        return values

    def getEarliestDay(self):
        return getEarliestDay(self.activityByDay, self.lastDay)
        
    def __getitem__(self, date):
        return self.activityByDay[asDateKey(date)]

    def __setitem__(self, date, value):
        self.activityByDay[asDateKey(date)] = float(value)

    def __delitem__(self, date):
        self.activityByDay.__delitem__(asDateKey(date))

    def __contains__(self, date):
        return self.activityByDay.__contains__(asDateKey(date))

if __name__ == "__main__":
    lastDay = dateParser.parse(sys.argv[1])
    ra = RecentActivity(lastDay)
    for arg in sys.argv[2:]:
        (name, value) = string.split(arg, '=')
        ra[name] = value
    va = ra.convertToValueArray()
    print(va)
