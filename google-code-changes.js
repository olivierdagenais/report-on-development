/*
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
*/
var feedUrlTemplate = "http://code.google.com/feeds/p/%PROJECT%/svnchanges/basic?path=%PATH%";
var chartImageTemplate = "<img src='http://chart.apis.google.com/chart?%CHART%' />";
var prefs = new gadgets.Prefs();
var projectName = prefs.getString("projectName");
var projectPath = prefs.getString("projectPath");
var entries = 50;

function _hesc(str) {
  // '<' and '>'
  str = str.replace(/</g, "&lt;").replace(/>/g, "&gt;");
  // '"' and '
  str = str.replace(/"/g, "&quot;").replace(/'/g, "&#39;");

  return str;
}

function getFeed() {
  var params = {};
  params[gadgets.io.RequestParameters.CONTENT_TYPE] = gadgets.io.ContentType.FEED;
  params[gadgets.io.RequestParameters.NUM_ENTRIES] = new Number(entries);
  var feedUrl = feedUrlTemplate.replace("%PROJECT%", _hesc(projectName)).replace("%PATH%", _hesc(projectPath));
  gadgets.io.makeRequest(feedUrl, response, params);
}

function addData(chart, data)
{
  var len = data.length;
  var max = 0;
  for (var i = 0; i < len; i++)
  {
    if (data[i] > max)
    {
      max = data[i];
    }
  }
  chart.chds = "0," + max;
  chart.chxr = "0," + (len-1) + "0" + "|1,0," + max + "|2," + (len-1) + "0";
  chart.chd = max <= 61 ? simpleEncode(data, 61) : extendedEncode(data, max);
}

function serializeChart(chart)
{
  var s = "chof=png";
  for (var key in chart)
  {
    if (chart.hasOwnProperty(key))
    {
      s += "&" + key + "=" + chart[key];
    }
  }
  return s;
}

function response(obj) {
  var feed = obj.data;

  var chart = {};
  chart.cht = "lc";
  chart.chs = "450x150"; // TODO: initialize from Gadget's client area
  chart.chma = "30,15";  // TODO: determine if that will be enough room

  chart.chco = "00FF00";
  chart.chm = "B,d0efd0,0,0,0";
  chart.chxt = "x,y,x";
  chart.chxs = "0,000000,10,0,t" + "|1,000000,10,1,lt" + "|2,000000,10,0";

  // TODO: read data from feed into values
  var values = new Array(5,3,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,2);
  // TODO: emit these additional labels based on the feed data
  /*
chxl=2:|today|2009-10-04
chxp=2,0,18
  */

  addData(chart, values);
  var s = serializeChart(chart);
  document.getElementById('content_div').innerHTML = chartImageTemplate.replace("%CHART%", s);
}

gadgets.util.registerOnLoadHandler(getFeed);
