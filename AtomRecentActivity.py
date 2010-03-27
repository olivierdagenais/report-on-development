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
import urllib
import urllib2
from datetime import datetime
from BeautifulSoup import BeautifulSoup, CData
from RecentActivitySource import RecentActivitySource

class AtomRecentActivity(RecentActivitySource):
    def __init__(self, lastDay, feedUrl):
        RecentActivitySource.__init__(self, lastDay)
        self.feedUrl = feedUrl

    def collectData(self):
        opener = urllib2.build_opener()
        self.feedXml = BeautifulSoup(opener.open(self.feedUrl))

    def interpretData(self):
        feed = self.feedXml.first()
        for entry in feed.findAll('entry'):
            self.logEntryAsActivity(entry)

    def logEntryAsActivity(self, entry):
        self.recentActivity[entry.updated.text] += 1

if __name__ == "__main__":
    feedUrl = sys.argv[1]
    ara = AtomRecentActivity(datetime.utcnow(), feedUrl)
    ara.printTestChartHtml()
