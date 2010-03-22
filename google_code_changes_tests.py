from datetime import datetime
from BeautifulSoup import BeautifulSoup, CData
import unittest
import google_code_changes

class TestGlobalFunctions(unittest.TestCase):
    def test_hesc(self):
        self.assertEquals("", google_code_changes._hesc(""))
        self.assertEquals("nothing special", google_code_changes._hesc("nothing special"))
        self.assertEquals("&lt;element attributeName=&quot;attribute&#39;s value&quot; /&gt;",
                          google_code_changes._hesc("<element attributeName=\"attribute's value\" />"))

if __name__ == '__main__':
    unittest.main()
