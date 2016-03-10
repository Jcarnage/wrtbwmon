#!/usr/bin/python

import time, sys, getopt
import sqlClass
import reportClass
            
#####################################################
#  Parse the command line
#####################################################
def parseCmdLine(argv):
    Year = ''
    Month = ''
    Day = ''
    Hour = ''
    Minute = ''
    deviceId = 0
    CSV = True
    TABLE = False
    try:
      opts, args = getopt.getopt(argv,"h:Y:M:D:H:m:",["sum","tbl","deviceId="])
    except getopt.GetoptError:
      print 'test.py -Y <year> -M <month> -D <day> -H <hour> -m <minute> --sum'
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
         print 'test.py -Y <year> -M <month> -D <day> -H <hour> -m <minute> --sum'
         break;
        elif opt in ("-Y"):
            Year = arg
        elif opt in ("-M"):
             Month = arg
        elif opt in ("-D"):
             Day = arg
        elif opt in ("-H"):
             Hour = arg
        elif opt in ("-m"):
             Minute = arg
        elif opt in ("--sum"):
            CSV = False
        elif opt in ("--tbl"):
            TABLE = True
        elif opt in ("--deviceId"):
            deviceId = arg
#    print 'Request is: %s-%s-%s %s-%s"' % (Year,Month,Day,Hour,Minute)
    return(Year,Month,Day,Hour,Minute,CSV,TABLE,deviceId)



#####################################################
#  Main code starts here
#####################################################
if __name__ == "__main__":
    db = sqlClass.sqlAccess("netMonitor.sqlite")
    report = reportClass.sqlReport()
    (Year,Month,Day,Hour,Minute,CSV,TABLE,deviceId) = parseCmdLine(sys.argv[1:])
    #    print ("%s %s %s %s %s %s") % (Year,Month,Day,Hour,Minute,CSV)

    # *****************************************************************************
    # *****************************************************************************
    if (deviceId > 0 and Year != '' and Month != '' and Day != ''):
        (itemList, deviceName) = db.returnDeviceDailyInfo(Year, Month, Day, deviceId)
        tblFormat = report.printDeviceSummaryTable(itemList)
    #        print "Information for %s" % deviceName
        print tblFormat
    # *****************************************************************************
    # If we are provided with the YY MM DD information, then we are looking to 
    # get the reports for a day.   If the --sum option then a CSV output is provided
    # allowing for more data manipulation.  --sum results in more simple data broken
    # down by device
    # *****************************************************************************
    elif (Year != '' and Month != '' and Day != ''):
        itemList = db.returnDayValues(Year, Month, Day, CSV)
        deviceList = db.getAllDeviceNames()
        if itemList:
            if (CSV == False):
                report.printSummary(itemList, TABLE)
            elif (TABLE == True):
                tableItems = report.printDailySummary(itemList,deviceList)
                print tableItems
            else:
                report.printCsvDetails(itemList)
        else:
            print "There were no values returned from the database for that timeframe"
    # *****************************************************************************
    # *****************************************************************************
    elif(Year != '' and Month != ''):
        itemList = db.returnMonthValues(Year, Month, CSV)
        if (CSV == False):
            report.printSummary(itemList, TABLE)
        else:
            report.printCsvDetails(itemList)        
    else:
	    print "Nothing to do"    
    
#       print results
