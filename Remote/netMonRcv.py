import traceback

# Create an empty dictionary
macList = {}
glbHour = -1

class NetMonitor(object):

    def parseData(self, dataString, aString = True):
        if aString == True:
           # split the string across lines (using the \n char)
            myLines = dataString.split("\n")
            for line in myLines:
                self.addToDict(self.splitData(line))            
        else:
            for i in dataString:
                # It's possible that the list is one long line with \n separators
                myLines = i.split("\n")
                for line in myLines:
                    self.addToDict(self.splitData(line)) 


    # This will take our incoming string which is MAC, DATAIN, DATAOUT
    # and split it into a list.  The list will be returned
    def splitData(self, myString):
        if ((len(myString) > 10) and (myString.count(',') == 2)):
            # Split the string into the three items
            try:
                items = myString.split(",")
                items[1] = int(items[1])
                items[2] = int(items[2])
                return items
            except Exception as e:
                if self.logger:
                    self.logger.error(("Received improper in splitData. Message : %s") % (myString))
        else:
            return None


    # This function will update/modify the global dictionary.  A list of 3 
    # items (MAC, dataIn, dataOut) must be passed to this function.  
    # NOTE: Only the size of the list is checked before being acted on
    def addToDict(self, items):
        if (items != None):
            if (len(items) == 3):
                # Check to see if item 1 exists into our array and if it does
                # we update the values of the counts
                if items[0] in macList:
                    i = macList[items[0]]
                    # Data Out
                    i[0] += items[1]
                    # Data In
                    i[1] += items[2]
                    macList[items[0]] =  [i[0], i[1]]
                # If the item doesn't exist we need to add it
                else:
                    macList[items[0]] = [items[1],items[2]]

    def clearDictionary():
        macList.clear()


    def __init__(self, logger):
        self.logger = logger



