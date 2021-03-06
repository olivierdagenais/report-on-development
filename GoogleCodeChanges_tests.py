﻿"""
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
import unittest
from datetime import datetime
import GoogleCodeChanges

class TestGlobalFunctions(unittest.TestCase):
    def test_hesc(self):
        self.assertEquals("", GoogleCodeChanges._hesc(""))
        self.assertEquals("nothing special", GoogleCodeChanges._hesc("nothing special"))
        self.assertEquals("&lt;element attributeName=&quot;attribute&#39;s value&quot; /&gt;",
                          GoogleCodeChanges._hesc("<element attributeName=\"attribute's value\" />"))

    def testconstructor(self):
        gcc = GoogleCodeChanges.GoogleCodeChanges(datetime(2010, 03, 26), "report-on-development", "trunk")
        self.assertEquals(
            "http://code.google.com/feeds/p/report-on-development/svnchanges/basic?path=trunk",
            gcc.feedUrl)

if __name__ == '__main__':
    unittest.main()
