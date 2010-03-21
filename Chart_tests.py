import unittest
import Chart

class TestGlobalFunctions(unittest.TestCase):

    def testaxisRange(self):
        self.assertEquals("0,0,0", Chart.axisRange(0, 0, 0))
        self.assertEquals("0,0.0,42.0", Chart.axisRange(0, 0.0, 42.0, 0))
        self.assertEquals("0,0,42,1", Chart.axisRange(0, 0, 42, 1))

    def testcomputeAxisRanges(self):
        actual = Chart.computeAxisRanges(1, 42, 450, 150)
        self.assertEquals("0,0,0,1|1,0,42|2,0,0", actual)

    def testaddDataSimple(self):
        c = Chart.Chart()
        c.chs = "450x150"
        c.addData([12, 40, 39, 36, 30, 50, 44])
        self.assertEquals("0,50", c.chds)
        self.assertEquals("0,6,0,1|1,0,50|2,6,0", c.chxr)
        self.assertEquals("s:Pxwsl92", c.chd)

    def testaddDataExtended(self):
        c = Chart.Chart()
        c.chs = "450x150"
        c.addData([808, 2532, 1970, 2879])
        self.assertEquals("0,2879", c.chds)
        self.assertEquals("0,3,0,1|1,0,2879|2,3,0", c.chxr)
        self.assertEquals("e:R94Rry..", c.chd)

    def teststrEmpty(self):
        c = Chart.Chart()
        self.assertEquals("chof=png", c.str())

    def teststrOnePair(self):
        c = Chart.Chart()
        c.name = "value"
        self.assertEquals("chof=png&name=value", c.str())

    def teststrWithValue(self):
        c = Chart.Chart()
        c.chs = "450x150"
        c.addData([42])
        self.assertEquals("chof=png&chd=s:9&chds=0,42&chs=450x150&chxr=0,0,0,1|1,0,42|2,0,0", c.str())

    def testasImgElement(self):
        c = Chart.Chart()
        c.chco = "00FF00"
        c.chs = "450x150"
        c.addData([42])
        actual = c.asImgElement()
        self.assertEquals("<img src='http://chart.apis.google.com/chart?"
                          + "chof=png"
                          + "&chco=00FF00"
                          + "&chd=s:9"
                          + "&chds=0,42"
                          + "&chs=450x150"
                          + "&chxr=0,0,0,1|1,0,42|2,0,0"
                          + "' />", actual)

if __name__ == '__main__':
    unittest.main()
