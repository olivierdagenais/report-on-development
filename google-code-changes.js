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
  chart.chxr = "0," + (len-1) + ",0" + "|1,0," + max + "|2," + (len-1) + ",0";
  chart.chd = max <= 61 ? simpleEncode(data, max) : extendedEncode(data, max);
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

function beginningOfDay(date)
{
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

function nextDay(date)
{
  // "November 31st" is converted to "December 1st", so this works
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1);
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

  var milliSecondsPerDay = 1000 * 60 * 60 * 24;
  var commitsByDay = {};
  var todayMilliSeconds = beginningOfDay(new Date()).getTime();
  var earliestDayMilliSeconds = todayMilliSeconds + milliSecondsPerDay; // "tomorrow"
  if (feed.Entry)
  {
    for (var i = 0; i < feed.Entry.length; i++)
    {
      var date = new Date(feed.Entry[i].Date);
      var dayKey = beginningOfDay(date).getTime();
      if (dayKey < earliestDayMilliSeconds)
      {
        earliestDayMilliSeconds = dayKey;
      }

      if (!commitsByDay.hasOwnProperty(dayKey))
      {
        commitsByDay[dayKey] = 0;
      }
      commitsByDay[dayKey]++;
    }
  }

  var currentDay = new Date(earliestDayMilliSeconds);
  var values = new Array();
  while (currentDay.getTime() <= todayMilliSeconds)
  {
    if (commitsByDay.hasOwnProperty(currentDay.getTime()))
    {
      values.push(commitsByDay[currentDay.getTime()]);
    }
    else
    {
      values.push(0);
    }
    currentDay = nextDay(currentDay);
  }

  addData(chart, values);

  var earliestDate = new Date(earliestDayMilliSeconds);
  chart.chxl = "2:|today|" + earliestDate.toLocaleDateString();
  chart.chxp = "2,0," + (values.length - 1);

  var s = serializeChart(chart);
  document.getElementById('content_div').innerHTML = chartImageTemplate.replace("%CHART%", s);
}

gadgets.util.registerOnLoadHandler(getFeed);
