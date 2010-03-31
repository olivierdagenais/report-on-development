from datetime import datetime
from urllib import urlretrieve
from shutil import copyfile
from tempfile import mkstemp
from os import remove, close

import settings
from FogBugzTime import FogBugzTime, asIso8601zDateString
from GoogleCodeChanges import GoogleCodeChanges
from HudsonBuilds import HudsonBuilds

def processAndDownload(today, dict, width, height, destFolder):
    lastUpdated = "last+updated+%s" % asIso8601zDateString(today)
    for (name, source) in dict.iteritems():
        print name,
        (tempHandle, tempPath) = mkstemp()
        close(tempHandle)
        try:
            print '.',
            source.collectData()
            print '.',
            source.interpretData()
            print '.',
            chart = source.renderChart(width, height)
            chart.chtt = lastUpdated
            chart.chts = "000000,9"
            filename = "%s-%dx%d.png" % (name, width, height)
            print '.',
            urlretrieve(chart.asUrl(), tempPath)
            print '.',
            copyfile(tempPath, destFolder + "/" + filename)
            print '!'
        except Exception, e:
            print("[%s] Unable to update %s: %s" % (datetime.utcnow(), name, e))
        finally:
            remove(tempPath)

if __name__ == '__main__':
    # 380x230 and then also in individual pages (600x500)
    today = datetime.utcnow()
    images = { }
    images["todd-commits"] = GoogleCodeChanges(today, "testoriented", "/todd/trunk")
    images["todd-builds"] = HudsonBuilds(today, settings.HudsonUrl, "TODD")
    images["todd-time"] = FogBugzTime(today, settings.FogBugzUrl, settings.FogBugzUser, settings.FogBugzPassword)
    
    processAndDownload(today, images, 380, 230, "dashboard")
