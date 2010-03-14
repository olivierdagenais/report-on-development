// Copy-pasted from
// http://code.google.com/apis/chart/docs/data_formats.html#encoding_data
// on 2010/03/13

var simpleEncoding = 
  'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

// This function scales the submitted values so that
// maxVal becomes the highest value.
function simpleEncode(valueArray,maxValue) {
  var chartData = ['s:'];
  for (var i = 0; i < valueArray.length; i++) {
    var currentValue = valueArray[i];
    if (!isNaN(currentValue) && currentValue >= 0) {
    chartData.push(simpleEncoding.charAt(Math.round((simpleEncoding.length-1) * 
      currentValue / maxValue)));
    }
      else {
      chartData.push('_');
      }
  }
  return chartData.join('');
}

// Same as simple encoding, but for extended encoding.
var EXTENDED_MAP=
  'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.';
var EXTENDED_MAP_LENGTH = EXTENDED_MAP.length;
function extendedEncode(arrVals, maxVal) {
  var chartData = 'e:';
  for(i = 0, len = arrVals.length; i < len; i++) {
    // In case the array vals were translated to strings.
    var numericVal = new Number(arrVals[i]);

    // Scale the value to maxVal.
    var scaledVal = Math.round(EXTENDED_MAP_LENGTH * 
        EXTENDED_MAP_LENGTH * numericVal/maxVal);

    if(scaledVal > EXTENDED_MAP_LENGTH * EXTENDED_MAP_LENGTH - 1) ||
       scaledVal > maxVal) {
      scaledVal = maxVal;
    } else if (scaledVal < 0) {
      chartData += '__';
      continue;
    } else {
      // Calculate first and second digits and add them to the output.
      var quotient = Math.floor(scaledVal / EXTENDED_MAP_LENGTH);
      var remainder = scaledVal - EXTENDED_MAP_LENGTH * quotient
      chartData += EXTENDED_MAP.charAt(quotient) + EXTENDED_MAP.charAt(remainder);
    }
  }
  return chartData;
}