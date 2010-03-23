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
import string
import chart_encoding

chartImageUrl = "http://chart.apis.google.com/chart?"
chartImageTemplate = "<img src='%(url)s' width='%(width)d' height='%(height)d' />"
minPixelsBetweenHorizontalAxisValues = 13
minPixelsBetweenVerticalAxisValues = 13

def axisRange(axisIndex, startVal, endVal, step = 0):
    # startVal and endVal are integers or floats, but %f will emit "42.0000" for "42.0", while %s emits "42.0"
    if 0 == step:
        result = "%d,%s,%s" % ( axisIndex, startVal, endVal )
    else:
        result = "%d,%s,%s,%d" % ( axisIndex, startVal, endVal, step )
    return result

def computeAxisRanges(numValues, maxValue, chartWidth, chartHeight):
    axes = []
    numPixelsPerDay = chartWidth / numValues
    axes.append(axisRange(0, numValues - 1, 0, 1 if numPixelsPerDay >= minPixelsBetweenHorizontalAxisValues else 0))
    numPixelsPerValue = chartHeight / maxValue
    axes.append(axisRange(1, 0, maxValue, 1 if numPixelsPerValue >= minPixelsBetweenVerticalAxisValues else 0))
    axes.append(axisRange(2, numValues - 1, 0))
    return string.join(axes, "|")

class Chart:
    def __init__(self):
        # TODO: accept named parameters, etc.
        pass

    def getDimensions(self):
        width, height = string.split(self.chs, 'x')
        width, height = int(width), int(height)
        return width, height

    def addData(self, data):
        length = len(data)
        max = 0
        for datum in data:
            if datum > max:
                max = datum
        self.chds = "0," + str(max)

        width, height = self.getDimensions()
        # Accounts for margins and axis labels (up to 5 significant digits on the Y axis and 2 rows on the X axis)
        effectiveWidth, effectiveHeight = width - 50, height - 40
        self.chxr = computeAxisRanges(length, max, effectiveWidth, effectiveHeight)
        self.chd = chart_encoding.simpleEncode(data, max) if max <= 61 else chart_encoding.extendedEncode(data, max)

    def str(self):
        s = "chof=png"
        for key in dir(self):
            if not key.startswith("__"):
                attr = getattr(self, key)
                if isinstance(attr, basestring): # skip instance methods, etc.
                    s += "&" + key + "=" + attr 
        return s

    def asUrl(self):
        url = chartImageUrl + self.str()
        return url

    def asImgElement(self):
        url = self.asUrl()
        width, height = self.getDimensions()
        imgElement = chartImageTemplate % { "url" : url, "width" : width, "height" : height }
        return imgElement

if __name__ == "__main__":
    c = Chart()
    data = []
    for arg in sys.argv:
        if arg.startswith('ch') and string.find(arg, '=') > 0: 
            (name, value) = string.split(arg, '=')
            setattr(c, name, value)
        elif chart_encoding.is_number(arg):
            data.append(float(arg))
    if len(data) > 0:
        c.addData(data)
    print(c.str())
