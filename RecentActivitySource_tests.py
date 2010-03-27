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
import collections
from datetime import datetime
import unittest
import Chart
import RecentActivitySource
import RecentActivity

class TestGlobalFunctions(unittest.TestCase):

    def testrenderMetadata(self):
        c = Chart.Chart()
        RecentActivitySource.renderMetadata(c, datetime(2010, 01, 01), 2)
        self.assertEquals("2:|today|2010/01/01", c.chxl)
        self.assertEquals("2,0,1", c.chxp)

if __name__ == '__main__':
    unittest.main()
