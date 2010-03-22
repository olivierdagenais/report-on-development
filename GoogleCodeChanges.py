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
from datetime import datetime
from AtomRecentActivity import AtomRecentActivity

feedUrlTemplate = "http://code.google.com/feeds/p/%PROJECT%/svnchanges/basic?path=%PATH%";

def _hesc(str):
    # '<' and '>'
    str = str.replace("<", "&lt;").replace(">", "&gt;")
    # '"' and '
    str = str.replace('"', "&quot;").replace("'", "&#39;")

    return str

class GoogleCodeChanges(AtomRecentActivity):
    def __init__(self, projectName, projectPath, lastDay):
        feedUrl = feedUrlTemplate.replace("%PROJECT%", _hesc(projectName)).replace("%PATH%", _hesc(projectPath))
        AtomRecentActivity.__init__(self, feedUrl, lastDay)

if __name__ == "__main__":
    projectName = sys.argv[1];
    projectPath = sys.argv[2];
    gcc = GoogleCodeChanges(projectName, projectPath, datetime.utcnow())
    gcc.fetchFeed()
    gcc.interpretFeed()
    print(gcc.createChartHtml())
