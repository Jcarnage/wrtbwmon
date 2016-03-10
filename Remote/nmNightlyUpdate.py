#!/usr/bin/env python

import sys, getopt

import sqlClass
import reportClass

import support

dbase = "netMonitor.sqlite"
# This script is run nightly (after midnight) to perform certain updates to 
# the database.   These updates include:
#   - create a daily summary (data in out)
#   - clean up date database (vaccum)
#   - create an index.html with the most recent dates available in the database

# This function will update the database.  It will summarize the information for 
# the relevant day (information passed in as 3 disctinct variables for Year, Month, Day)
 

##########################################################################
#  Parse the command line.  If there's no valid date information provided
#  to us as an option, then return the current date
##########################################################################
def parseCmdLine(argv):
    (Year, Month, Day) = support.getDateYesterday()

    try:
      opts, args = getopt.getopt(argv,"h:Y:M:D:",[])
    except getopt.GetoptError:
      print 'test.py -Y <year> -M <month> -D <day>'
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
         print 'test.py -Y <year> -M <month> -D <day>'
         break;
        elif opt in ("-Y"):
            Year = arg
        elif opt in ("-M"):
             Month = arg
        elif opt in ("-D"):
             Day = arg
    print 'Request is: %s-%s-%s' % (Year,Month,Day)
    return(int(Year),int(Month),int(Day))

##########################################################################
def updateDatabase():
    db = sqlClass.sqlAccess(dbase)
    (YY, MM, DD) = parseCmdLine(sys.argv[1:])
    data = [0, 0]
    itemList = db.returnDayValues(YY, MM, DD, True)

    if itemList:
        for item in itemList:
            data[0] += item[1]
            data[1] += item[2]
    db.updateDailySummary(YY, MM, DD, data[0], data[1])
    db.closeConnection()



if __name__ == "__main__":
    updateDatabase()
