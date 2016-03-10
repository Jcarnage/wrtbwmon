#!/usr/bin/env python

import cgi,os,sys
import cgitb
import time

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


def main(tableValues, Year, Month, Day):
	searchDate = str(Year) + "-" + str(Month) + "-" + str(Day)

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
			  title: 'Broughton Daily Usage : %s',
			  width: 1100,
			  height: 500,
			  isStacked: true,
			  backgroundColor: '#808090',
			  hAxis: {title: 'Date', titleTextStyle: {color: 'white'}},
			  vAxis: {title: 'Bandwith (KB)', titleTextStyle: {color: 'white'}},
			  chartArea: {
		    		backgroundColor: {
		        		stroke: '#fff',
		        		strokeWidth: 1
		    		}
				},
			  /*colors: ['green','yellow'],		*/    	
			};

			var chart = new google.visualization.ColumnChart
					(document.getElementById('chart_div'));
			chart.draw(data, options);
		  }
		</script>
        </body>
		<div id="chart_div"></div> """ % (tableValues, searchDate)
	else:
		page_str += """
		<div id="error">There is no data for the date provided</div>
		"""

	page_str += """	</br></br>
	<div id="form_entry">
	<form action="/cgi-bin/dailyReport.py" method="post">
	Year: <input type="text" name="Year" size=5 maxLength=4 value="%s" />
	Month: <input type="text" name="Month" size=2 maxLength=2 value="%s" />
	Day: <input type="text" name="Day" size=2 maxLength=2 value="%s" />	
	<input type="submit" value="Submit" />
	</form>     
	</div>
	""" %  (str(Year), str(Month), str(Day))

	(nYear, nMonth, nDay) = support.yesterday(Year, Month, Day)
	page_str +=  """
	<div id="previous">
	<a id="prevButton" href="/cgi-bin/dailyBwReport.py?Year=%s&Month=%s&Day=%s">Previous</a> 
	</div>"""  % (nYear, nMonth, nDay)

	(nYear, nMonth, nDay) = support.tomorrow(Year, Month, Day)
	page_str +=  """
	<div id="next">
	<a id="nextButton" href="/cgi-bin/dailyBwReport.py?Year=%s&Month=%s&Day=%s">Next</a> 
	</div>"""  % (nYear, nMonth, nDay)
	
	page_str +=  """</body>""" 
	
	# serve the page with the data table embedded in it
	print page_str

def getDefaultDate():
	myDate = time.localtime()
	return (myDate.tm_year, myDate.tm_mon, myDate.tm_mday)	

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
    except:
        (YY, MM, DD) = getDefaultDate()
        MM = 2
        DD = 28

    itemList = db.returnDayValues(YY, MM, DD, True)
    deviceList = db.getAllDeviceNames()
    if (itemList is not None):
	    parameters = report.printDailySummary(itemList,deviceList)	
    #	print parameter	
	    main(parameters,YY,MM,DD)
    else:
	    main(None, YY, MM,DD)
