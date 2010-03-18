"""
Ported from code at:
http://code.google.com/apis/chart/docs/data_formats.html#encoding_data
retrieved 2010/03/13
"""
import string
import math

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

simpleEncoding = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
simpleEncodingLength = len(simpleEncoding)
"""
This function scales the submitted values so that
maxVal becomes the highest value.
"""
def simpleEncode(valueArray,maxValue):
    chartData = ['s:']
    for currentValue in valueArray:
        if is_number(currentValue) and currentValue >= 0:
            chartData.append(simpleEncoding[int(round((simpleEncodingLength - 1) * currentValue / maxValue))])
        else:
            chartData.append('_')

    return string.join(chartData, '')


EXTENDED_MAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.'
EXTENDED_MAP_LENGTH = len(EXTENDED_MAP)
EXTENDED_RANGE = EXTENDED_MAP_LENGTH * EXTENDED_MAP_LENGTH - 1
"""
Same as simple encoding, but for extended encoding.
"""
def extendedEncode(arrVals, maxVal):
    chartData = 'e:'
    for numericVal in arrVals:

        # Scale the value to maxVal.
        scaledVal = round(EXTENDED_RANGE * numericVal/maxVal)

        if scaledVal > EXTENDED_RANGE or scaledVal > maxVal:
            scaledVal = maxVal
        elif scaledVal < 0:
            chartData += '__'
            continue
        else:
            # Calculate first and second digits and add them to the output.
            quotient = math.floor(scaledVal / EXTENDED_MAP_LENGTH)
            remainder = scaledVal - EXTENDED_MAP_LENGTH * quotient
            chartData += EXTENDED_MAP[int(quotient)] + EXTENDED_MAP[int(remainder)]

    return chartData

