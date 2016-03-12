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


def main(tableValues, Year, Month):
    searchDate = str(Year) + "-" + str(Month) 

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
              title: 'Network Monthly Usage : %s',
              width: 1100,
              height: 500,
              isStacked: true,
              backgroundColor: '#808090',
              hAxis: {title: 'Day of Month', titleTextStyle: {color: 'white'}},
              vAxis: {title: 'Bandwith (MB)', titleTextStyle: {color: 'white'}},
              chartArea: {
            		backgroundColor: {
                		stroke: '#fff',
                		strokeWidth: 1
            		}
	            },
              colors: ['blue','yellow'],		    	
            };

            var chart = new google.visualization.ColumnChart
		            (document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script><body>
        <div id="chart_div"></div> """ % (tableValues, searchDate)
    else:
        page_str += """<body>
        <div id="error">There is no data for the date provided</div>
        """

    page_str += """	</br></br>
    <div id="form_entry">
    <form action="/cgi-bin/monthlyReport.py" method="post">
    Year: <input type="text" name="Year" size=5 maxLength=4 value="%s" />
    Month: <input type="text" name="Month" size=2 maxLength=2 value="%s" />
    <input type="submit" value="Submit" />
    </form>     
    </div>
    """ %  (str(Year), str(Month))

    (nYear, nMonth) = support.lastMonth(Year, Month)
    page_str +=  """
    <div id="previous">
    <a id="prevButton" href="/cgi-bin/monthlyReport.py?Year=%s&Month=%s">Previous</a> 
    </div>"""  % (nYear, nMonth)

    page_str += """<img id="image" src="/netMonitor/netMonitor.jpg" alt="Boxie" Title="netMonitor"/>
    """

    (nYear, nMonth) = support.nextMonth(Year, Month)
    page_str +=  """
    <div id="next">
    <a id="nextButton" href="/cgi-bin/monthlyReport.py?Year=%s&Month=%s">Next</a> 
    </div>"""  % (nYear, nMonth)
	
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
    except:
        (YY, MM, DD) = support.getDateToday()

    itemList = db.returnMonthlySummary(YY, MM)
    if (itemList is not None):
        (tableValues, dataInTotal, dataOutTotal) = report.printMonthlySummary(itemList, YY, MM)	
        main(tableValues,YY,MM)
    else:
        main(None, YY, MM)
