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
simpleRange = simpleEncodingLength - 1
"""
This function scales the submitted values so that
maxValue becomes the highest value.
"""
def simpleEncode(valueArray, maxValue):
    chartData = ['s:']
    for currentValue in valueArray:
        if is_number(currentValue) and currentValue >= 0:
            # Scale the value to maxValue
            scaledVal = round(simpleRange * currentValue / maxValue)

            if scaledVal <= simpleRange:
                chartData.append(simpleEncoding[int(scaledVal)])
                continue

        chartData.append('_')

    return string.join(chartData, '')


extendedEncoding = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.'
extendedEncodingLength = len(extendedEncoding)
extendedRange = extendedEncodingLength * extendedEncodingLength - 1
"""
Same as simple encoding, but for extended encoding.
"""
def extendedEncode(valueArray, maxValue):
    chartData = 'e:'
    for currentValue in valueArray:
        if is_number(currentValue) and currentValue >= 0:
            # Scale the value to maxValue
            scaledVal = round(extendedRange * currentValue / maxValue)

            if scaledVal <= extendedRange:
                # Calculate first and second digits and add them to the output.
                quotient = math.floor(scaledVal / extendedEncodingLength)
                remainder = scaledVal - extendedEncodingLength * quotient
                chartData += extendedEncoding[int(quotient)] + extendedEncoding[int(remainder)]
                continue

        chartData += '__'

    return chartData

