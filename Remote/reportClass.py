
import locale
import support

class sqlReport(object):
#####################################################
    def printSummary(self, ItemList, tblFormat):
        myVar = ''
        dataInTotal = 0
        dataOutTotal = 0
        dailyOutput = {}
        for row in ItemList:
            if row[3] in dailyOutput:
                thisRow = dailyOutput[row[3]]
                thisRow[0] = thisRow[0] + row[1]
                thisRow[1] = thisRow[1] + row[2]
            else:
                dailyOutput[row[3]] = [row[1],row[2]]

            dataInTotal = dataInTotal + row[1]
            dataOutTotal = dataOutTotal + row[2]

        if (tblFormat == False):                        
            print "Device                  DataOut (KB)     DataIn (KB)"
        else:
            myVar = "\n['Device','DataOut','DataIn'],\n"

        for item in dailyOutput:
            data = dailyOutput[item]
            if (tblFormat == False):
                print ("%-20s %10d %20d") % (item, data[1]/1024, data[0]/1024)
            else:
                myVar = myVar + "['" + item +"'," + str(data[1]/1024) + "," + str(data[0]/1024) + "]"
                myVar = myVar + ",\n"
        
        if (tblFormat == False):
            print ("Totals (MB):   DataOut: %7d    DataIn: %9d ") \
                % (dataOutTotal/1024, dataInTotal/1024)                
        if (myVar):
            return (myVar, dataInTotal, dataOutTotal)
            
#####################################################            
    def printCsvDetails(self,ItemList):            
        for row in ItemList:
            print ("%s,%s,%s,%s") %(row[0], row[1], row[2], row[3])

# *****************************************************************************
# The following is used to generate the networks daily usage table.  The table
# is based on the hour/minute and the information results in stacked columns
#
# Although the output is geared towards google chart, some post processing to 
# remove the [ and ]'s and we have a CSV ready for Excel/Calc
    def printDailySummary(self, ItemList, devices):
        divisor = 1048576
        lclDict = {}
        activeDevices = {}
        # The following is used to provide ordering for the dictionary
        time = []

        # The following for loop will stack the items in a a dictionary, in ways
        # that we can easily pull data out of (dictionary of dictionarys).  It's
        # easier to do it this way than to try to build the information on the fly
        for item in ItemList:
            if not item[0] in lclDict:
                lclDict[item[0]] = {}
                time.append(item[0])
              
            lclDict[item[0]][item[3]] = [item[1], item[2]] # [DataIn, DataOut]
            activeDevices[item[3]] = [""]
        # Create the header information
        var = "[ 'Time'" 
        for i in range(0, len(devices)):
            if devices[i] in activeDevices:
                var +=  ", '" + devices[i] + "'"
        var += " ],\n"
        # Use the time (which is ordered to build our charts in the proper sequence
        for item in time:
            var += "[ '"  + item +"'"
            # For each time value, get the ordered list of the various devices.
            for i in devices:
                if i in activeDevices:
                    if i in lclDict[item]:
                        var += ", " + str(lclDict[item][i][0]) # [Only look at dataIn (for now)
                # If a device was not active during this time frame pad it 0 (don't leave empty)
                    else:
                        var += ", 0"
            var += " ],\n"
        return var

# *****************************************************************************
# The following is used to generate the networks monthly usage table
    def printMonthlySummary(self, ItemList, Year, Month):
        daysOfMonth = support.getDaysInMonth(Year, Month)
        thisDay = 1
        divisor = 1024
        dataInTotal = 0
        dataOutTotal = 0
        myVar = "\n['Day','DataIn','DataOut'],\n"
        for row in ItemList:
            while thisDay != row[0]:
                myVar += "['" + str(thisDay) +"',0 , 0],\n"
                thisDay += 1
                if thisDay > daysOfMonth:
                    return (myVar, dataInTotal, dataOutTotal)

            myVar = myVar + "['" + str(row[0]) +"'," + str(row[1]/divisor) + "," + str(row[2]/divisor) + "]"
            myVar = myVar + ",\n"
            dataInTotal = dataInTotal + row[1]
            dataOutTotal = dataOutTotal + row[2]
            thisDay += 1
            if thisDay > daysOfMonth:
                break
        while thisDay <= daysOfMonth:
            myVar += "['" + str(thisDay) +"',0 , 0],\n"
            thisDay += 1
               
        return (myVar, dataInTotal, dataOutTotal)                

##########################################################################
# The following is used to generate the device daily usage table                
    def printDeviceSummaryTable(self, ItemList, hours):
        lclDict = {}
        myVar = ''
        # Prepare out dictionary with base data
        for i in hours:
            lclDict[i] = [0,0]
        # Update our dictionary with real data, and the gaps will be 0,0
        for i in ItemList:
            lclDict[i[0]] = [i[1], i[2]]

        dataInTotal = 0
        dataOutTotal = 0
        myVar = "\n['Time','DataOut','DataIn'],\n"        
        for i in hours:
            j = lclDict[i]
            myVar = myVar + "['" + i +"'," + str(j[1]) + "," + str(j[0]) + "]"
            myVar = myVar + ",\n"
            dataInTotal = dataInTotal + j[0]
            dataOutTotal = dataOutTotal + j[1]
        return (myVar)    
        
    
