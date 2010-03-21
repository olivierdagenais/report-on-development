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

chartImageTemplate = "<img src='http://chart.apis.google.com/chart?%CHART%' />";

def axisRange(axisIndex, startVal, endVal, step = 0):
    # startVal and endVal are integers or floats, but %f will emit "42.0000" for "42.0", while %s emits "42.0"
    if 0 == step:
        result = "%d,%s,%s" % ( axisIndex, startVal, endVal )
    else:
        result = "%d,%s,%s,%d" % ( axisIndex, startVal, endVal, step )
    return result

def computeAxisRanges(numValues, maxValue, chartWidth, chartHeight):
    axes = []
    # TODO: step can be 1 if numValues < 30 (for a chart width of 450)
    axes.append(axisRange(0, numValues - 1, 0))
    # TODO: step of 1 only makes sense when maxValue is < 15 (for a chart height of 50)
    axes.append(axisRange(1, 0, maxValue, 1))
    axes.append(axisRange(2, numValues - 1, 0))
    return string.join(axes, "|")

class Chart:
    def __init__(self):
        # TODO: accept named parameters, etc.
        pass

    def addData(self, data):
        length = len(data)
        max = 0
        for datum in data:
            if datum > max:
                max = datum
        self.chds = "0," + str(max)

        width, height = string.split(self.chs, 'x')
        self.chxr = computeAxisRanges(length, max, int(width), int(height))
        self.chd = chart_encoding.simpleEncode(data, max) if max <= 61 else chart_encoding.extendedEncode(data, max)

    def str(self):
        s = "chof=png"
        for key in dir(self):
            if not key.startswith("__"):
                attr = getattr(self, key)
                if isinstance(attr, basestring): # skip instance methods, etc.
                    s += "&" + key + "=" + attr 
        return s

    def asImgElement(self):
        s = self.str()
        imgElement = chartImageTemplate.replace("%CHART%", s)
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
