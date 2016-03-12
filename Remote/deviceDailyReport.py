#!/usr/bin/env python

import cgi,os,sys
import cgitb
import time
import datetime

sys.path.append('data')
import support
import sqlClass
import reportClass

# enable tracebacks of exceptions
cgitb.enable()

# print an HTTP header
#
def printHTTPheader():
    print "Content-type: text/html"
    print ""
    print ""


def main(tableValues, Year, Month, Day, ID, deviceDict):
    searchDate = str(Year) + "-" + str(Month) + "-" + str(Day)
    dropDownItems = ''
    ########  Prepare information for Dropdown ###################
    for item in deviceDict:
        if item == ID:
            dropDownItems += "<option value=\"" + str(item) + "\" selected>" + deviceDict[item] + "</option>\n"
        else:
            dropDownItems += "<option value=\"" + str(item) + "\">" + deviceDict[item] + "</option>\n"
	
    printHTTPheader()

    # this string contains the web page that will be served
    page_str="""
    <head>
	    <link type="text/css" rel="stylesheet" href="/netMonitor/stylesheet.css"/>
    </head>

    <h1>PAGE_TITLE</h1>"""

    if (tableValues is not None):
        page_str += """
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([%s]);

            var options = {
              title: 'Bandwdith Usage on: %s for device %s ' ,
              width: 1100,
              height: 500,
              isStacked: true,
              backgroundColor: '#808090',
              hAxis: {title: 'Date', titleTextStyle: {color: 'white'}},
              vAxis: {title: 'Bandwith (B)', titleTextStyle: {color: 'white'}},
              chartArea: {
            		backgroundColor: {
                		stroke: '#fff',
                		strokeWidth: 1
            		}
	            },
              colors: ['green','yellow'],		    	
            };

            var chart = new google.visualization.ColumnChart
		            (document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>
        <div id="chart_div"></div>""" % (tableValues, searchDate, deviceDict[ID])
    else:
        page_str += """
        <div id="error">There is no data for the date provided</div>
        """

    page_str += """
    </br></br>
    <div id="form_entry">
    <form action="/cgi-bin/deviceDailyReport.py" method="post">
    Year: <input type="text" name="Year" size=5 maxLength=4 value="%s" />
    Month: <input type="text" name="Month" size=2 maxLength=2 value="%s" />
    Day: <input type="text" name="Day" size=2 maxLength=2 value="%s" />	
    Device: <select name="dropdown"> %s </select>		
    <input type="submit" id="submit", value="Submit" />
    </form>     
    </div>
    """ % (str(Year), str(Month), str(Day), dropDownItems)

    (nYear, nMonth, nDay) = support.yesterday(Year, Month, Day)
    page_str +=  """
    <div id="previous">
    <a id="prevButton" href="/cgi-bin/deviceDailyReport.py?Year=%s&Month=%s&Day=%s&dropdown=%s">Previous</a> 
    </div>"""  % (nYear, nMonth, nDay, ID)

    page_str += """<img id="image" src="/netMonitor/netMonitor.jpg" alt="Boxie" Title="netMonitor"/>
    """

    (nYear, nMonth, nDay) = support.tomorrow(Year, Month, Day)
    page_str +=  """
    <div id="next">
    <a id="nextButton" href="/cgi-bin/deviceDailyReport.py?Year=%s&Month=%s&Day=%s&dropdown=%s">Next</a> 
    </div>"""  % (nYear, nMonth, nDay, ID)

    page_str +=  """</body>""" 

    # serve the page with the data table embedded in it
    print page_str


if __name__=="__main__":
    db = sqlClass.sqlAccess("data/netMonitor.sqlite")
    report = reportClass.sqlReport()
    # Create instance of field storage
    form = cgi.FieldStorage()
    # Get data from the fileds
    try:
        YY = int(form.getvalue('Year'))
        MM = int(form.getvalue('Month'))
        DD = int(form.getvalue('Day'))
        ID = int(form.getvalue('dropdown'))		
    except:
        (YY, MM, DD) = support.getDateToday()
        ID = 1

    deviceDict = db.getDeviceList()
    itemList = db.returnDeviceDailyInfo(YY, MM, DD, ID)
    hours = db.getRecordingIntervals(YY, MM, DD)
    if (itemList is not None):
        parameters = report.printDeviceSummaryTable(itemList, hours)	
        main(parameters,YY,MM,DD,ID, deviceDict)
    else:
        main(None, YY,MM,DD,ID, deviceDict)
