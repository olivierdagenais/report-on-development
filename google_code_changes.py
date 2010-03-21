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
from BeautifulSoup import BeautifulSoup, CData
from Chart import Chart
from RecentActivity import RecentActivity

feedUrlTemplate = "http://code.google.com/feeds/p/%PROJECT%/svnchanges/basic?path=%PATH%";

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

def response(obj, lastDay):
    feed = obj.first()

    ra = RecentActivity(lastDay)
    for entry in feed.findAll('entry'):
        ra[entry.updated.text] += 1

    chart = ra.createChart()

    html = chart.asImgElement()
    return html

if __name__ == "__main__":
    projectName = sys.argv[1];
    projectPath = sys.argv[2];
    resp = getFeed(projectName, projectPath)
    print(response(resp, datetime.utcnow()))
