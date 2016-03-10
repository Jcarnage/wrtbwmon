#!/usr/bin/python

import socket
import time, sys
import select
import sqlClass
import logging
import logging.handlers
from netMonRcv import NetMonitor
from netMonRcv import macList
#from daemon import Daemon

dbName = "netMonitor.sqlite"
# We are going to be listening on port 5000
port = 5000
# Set our recording interval to 10s.
interval = 900

class trafficRecorder(object):

    def dataStore(self, dictList):
        q = sqlClass.sqlAccess(dbName)
        q.storeData(dictList)

    def setupLogging(self):
    ################### Set up our logging ########################
        netLogging = logging.getLogger('monitor.py')
        netLogging.setLevel(logging.DEBUG)

        handler = logging.handlers.SysLogHandler(address = '/dev/log')
    #       handler = logging.handlers.SysLogHandler(address = ('localhost',514), facility=19)
        netLogging.addHandler(handler)
        return netLogging
    ###############################################################


    def run(self):
        # Create a listening socket and make sure to seet it as non-blocking
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(0)
        s.bind(("", port))
        logger = self.setupLogging()

        logger.info(("Netmonitor Started. Waiting on port: %d") % (port))
        oldTime = int(time.time())
        # Instantiate the monitor class
        netMon = NetMonitor(logger)
        rcvFlag = False
        while 1:
            readable, _, exceptional = select.select([s],[],[s],1)
            if s in readable:
                data, addr = s.recvfrom(1024)
                netMon.parseData(data)
                rcvFlag = True
                time.sleep(1)
            else:
            # If we have received data, we will send it to our debug log and 
            # clear our flag.  This should help with getting data in chunks
            # so that we print it out only once in the log (rather than 
            # multiple times.
                if rcvFlag == True:
                    logger.debug(("Received : %s") % (macList,))
                    rcvFlag = False

                newTime = int(time.time())
                if ((newTime - oldTime) > interval):
                    logger.debug(("900s elapsed....%d") % (newTime))
                    #  This is where we will call our database
                    self.dataStore(macList)
                    macList.clear()
                    oldTime = newTime
                time.sleep(4)


if __name__ == "__main__":
    myDaemon = trafficRecorder()
    myDaemon.run()


