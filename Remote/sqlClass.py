import sqlite3
import time

class sqlAccess(object):
    dbConnect = False
    lastDateId = 0
    conn = 0

#  Consider the following methods private and don't use them for outside the class
    def _create_database(self, connector):
        sql = "CREATE TABLE 'tblData' ('dataId' INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , 'macId' INTEGER NOT NULL ,"
        sql = sql + "'dateId' INTEGER NOT NULL , 'dataIn' INTEGER NOT NULL , 'dataOut' INTEGER);"
        connector.execute(sql)
        sql = "CREATE TABLE 'tblDateInfo' ('dateId' INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , 'Year' INTEGER NOT NULL ,"
        sql = sql + "'Month' INTEGER NOT NULL , 'Day' INTEGER NOT NULL , 'Hour' INTEGER NOT NULL , 'Minute' INTEGER NOT NULL, "
        sql = sql + "'EpochSecs' INTEGER NOT NULL);"
        connector.execute(sql)
        sql = "CREATE TABLE 'tblMac' ('macId' INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , 'MAC' CHAR(20) NOT NULL , 'pcName' CHAR(50));"
        connector.execute(sql)
        sql = "CREATE TABLE 'tblDailySummary' ('sumId' INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , 'Year' INTEGER NOT NULL ,"
        sql =  sql + "'Month' INTEGER NOT NULL , 'Day' INTEGER NOT NULL , 'DataIn' INTEGER NOT NULL , 'DataOut' INTEGER NOT NULL )"
        connector.execute(sql)


    def _is_table_exists(self, connector):
        sql = "SELECT * FROM sqlite_master WHERE type='table' AND name='tblData'"
        if (not connector.execute(sql).fetchone()):
            self._create_database(connector)

    def _getDateId(self, YY, MM, DD, HH, SS):
        returnVal = 0
        sql = "SELECT dateId FROM tblDateInfo WHERE "
        sql += "Year ='%d' AND Month ='%d' AND Day = '%d' AND  Hour = '%d' AND Minute ='%d'" % (YY, MM, DD, HH, SS)
        cursor = self.conn.execute(sql)
        for row in cursor:
            returnVal = row[0]
        return returnVal

    def _writeDate(self, YY, MM, DD, HH, SS, Seconds):
        self.lastDateId = self._getDateId(YY, MM, DD, HH, SS)
        if (self.lastDateId == 0):
            sql = "INSERT INTO tblDateInfo (Year, Month, Day, Hour, Minute, EpochSecs) VALUES "
            sql += "('%d','%d','%d','%d','%d','%d')" % (YY, MM, DD, HH, SS, Seconds)
            self.conn.execute(sql)
            self.conn.commit()
            self.lastDateId = self._getLastInsertId()
        return self.lastDateId
        

    # Calling this function will generate a time stamp, write it to the database and then
    # return the index of the new date entry in the database
    def _timeStamp(self, seconds = None):
        if not(seconds == None):
            myDate = time.localtime(seconds)
            return (myDate.tm_year, myDate.tm_mon, myDate.tm_mday, myDate.tm_hour, myDate.tm_min, seconds)
        else:
            myDate = time.localtime()
            return self._writeDate(myDate.tm_year, myDate.tm_mon, myDate.tm_mday, myDate.tm_hour, myDate.tm_min, int(time.mktime(myDate)))

    def _getLastDateId(self):
        return self.lastDateId
    
    def _getDayRange(self, Year, Month, Day):
        cur = self.conn.cursor()
        cur.execute("SELECT dateId FROM tblDateInfo WHERE Year=? AND Month=? AND Day=?",(Year,Month,Day))
        rows = cur.fetchall()
        if rows:
            return (rows[0][0], rows[len(rows)-1][0])
        else:
            return (0, 0)

#    def _getDeviceName(self, deviceId):    
#        cur = self.conn.cursor()
#        print "This is our device ID: %s" % deviceId
#        cur.execute("SELECT pcName FROM tblMac WHERE macId=?" , (deviceId,))
#        row = cur.fetchone()
#        return row[0]

    def _getMacId(self, strMac):
        returnVal = 0
        sql = "SELECT macId FROM tblMac WHERE MAC = '" + strMac + "'"
        cursor = self.conn.execute(sql)
        for row in cursor:
            returnVal = row[0]
        return returnVal

    def _getLastInsertId(self):
        sql = "SELECT last_insert_rowid()"
        cursor = self.conn.execute(sql)
        self.conn.commit()
        for row in cursor:
            id = row[0]
        return id

    def _writeMac(self, macId, pcName):
        returnVal = self._getMacId(macId)
        if (returnVal == 0):
            returnVal = 0
            sql = "INSERT INTO tblMac (MAC, pcName) VALUES ('" + macId + "','" + pcName + "')"
            self.conn.execute(sql)
            self.conn.commit()
            returnVal = self._getLastInsertId()
        return returnVal

# End of private methods

    # ********************************************************************************
    # Returns a list of items with the following layout for each item:
    # (time, dataIn, dataOut, pcName)
    # ********************************************************************************
    def returnDayValues(self, Year, Month, Day, CSV=True):
        #print "We are looking for values related to a day"
        (firstId, lastId) = self._getDayRange(Year, Month, Day)
        if (firstId > 0 and lastId > firstId):
            cur = self.conn.cursor()
            cur.execute("SELECT strftime('%H:%M',tblDateInfo.EpochSecs,'unixepoch','localtime' ), \
            tblData.dataIn, tblData.dataOut, tblMac.pcName FROM tblData \
            JOIN tblMac \
            ON tblMac.macId = tblData.macId \
            JOIN tblDateInfo \
            ON tblDateInfo.dateId = tblData.dateId \
            WHERE tblDateInfo.dateId BETWEEN ? AND ?", (firstId, lastId));
            rows = cur.fetchall()
            if rows:
                return rows
        return None


    # ********************************************************************************
    # Returns a list of items with the following layout for each item:
    # (time (HH,MM), dataIn, dataOut)
    # ********************************************************************************
    def returnDeviceDailyInfo(self, Year, Month, Day, deviceId):
        #print "We are looking for values related to a month"
        (firstId, lastId) = self._getDayRange(Year, Month, Day)
        if (firstId > 0 and lastId > firstId):
            cur = self.conn.cursor()        
            cur.execute("SELECT strftime('%H:%M',tblDateInfo.EpochSecs,'unixepoch','localtime' ), \
            tblData.dataIn, tblData.dataOut FROM tblData \
            JOIN tblMac \
            ON tblMac.macId = tblData.macId \
            JOIN tblDateInfo \
            ON tblDateInfo.dateId = tblData.dateId \
            WHERE tblDateInfo.dateId BETWEEN ? AND ? AND tblMac.macId = ?", (firstId, lastId, deviceId));
            rows = cur.fetchall()
            if rows:
                return rows

        return None

    # ***********************************************************************************
    # For any given day, this function will return an ordered list of all times in HH:MM
    # format, that were recorded for that specific date 
    # Returns an array on success, else None is returned
    # ***********************************************************************************
    def getRecordingIntervals(self, Year, Month, Day):
        cur = self.conn.cursor()
        cur.execute("SELECT strftime('%H:%M',EpochSecs,'unixepoch','localtime' ) \
        FROM tblDateInfo WHERE Year=? AND Month=? AND Day=?",(Year, Month, Day))
        rows = cur.fetchall()
        if rows:
            _myArray = []
            for i in rows:
                _myArray.append(str(i[0]))
            return _myArray
        else:
            return None

    # ***********************************************************************************
    def returnMonthlySummary(self, Year, Month):
        cur = self.conn.cursor()        
        cur.execute("SELECT Day, DataIn, DataOut FROM tblDailySummary \
        WHERE Year=? AND Month=?",(Year,Month))
        rows = cur.fetchall()
        if rows:
            return rows
        else:
            return None

    # ***********************************************************************************
    def returnMonthValues(self, Year, Month, CSV=True):
        #print "We are looking for values related to a month"
        cur = self.conn.cursor()        
        cur.execute("SELECT dateId FROM tblDateInfo WHERE Year=? AND Month=?",(Year,Month))
        rows = cur.fetchall()
        if rows:
            firstId = rows[0][0]
            lastId = rows[len(rows)-1][0]
            if (firstId > 0 and lastId > firstId):
                cur.execute("SELECT date(tblDateInfo.EpochSecs,'unixepoch','localtime' ), \
                tblData.dataIn, tblData.dataOut, tblMac.pcName FROM tblData \
                JOIN tblMac \
                ON tblMac.macId = tblData.macId \
                JOIN tblDateInfo \
                ON tblDateInfo.dateId = tblData.dateId \
                WHERE tblDateInfo.dateId BETWEEN ? AND ?", (firstId, lastId));
                rows = cur.fetchall()
                return rows
        return None


    def getDeviceList(self):
        deviceName = {}
        cur = self.conn.cursor()
        cur.execute("SELECT macId, pcName FROM tblMac ORDER BY pcName COLLATE NOCASE")
        rows = cur.fetchall()
        idx = 0
        for row in rows:
            deviceName[idx] = [row[0], row[1]]
            idx += 1
        return deviceName

    def getAllDeviceNames(self):
        devices = []
        cur = self.conn.cursor()
        cur.execute("SELECT pcName FROM tblMac")
        rows = cur.fetchall()
        if rows:
            for i in rows:
                devices.append(str(i[0]))
            return devices
        else:
            return None
        
        
    def storeData(self, dictData):
        if dictData:
            #Generate a timestamp for the data we are about to record
            dateIndex = self._timeStamp()
            #Loop through the dictionary data
            for macKey in dictData.keys():
                macIndex = self._writeMac(macKey, macKey)
                i = dictData[macKey]
                sql = "INSERT INTO tblData (macId, dateId, dataOut, dataIn) "
                sql += "VALUES (%d, %d, %d, %d) " % (macIndex, dateIndex, i[0], i[1])
                self.conn.execute(sql)
            self.conn.commit()
            return 1
        else:
            return -1
            
    def getDailySummaryId(self, YY, MM, DD):
        sql = "SELECT sumId FROM tblDailySummary WHERE Year=%d AND Month=%d AND Day=%d " % (YY, MM, DD)
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            return 0

    def updateDailySummary(self, YY, MM, DD, dataIn, dataOut):
        id = self.getDailySummaryId(YY, MM, DD)
        if id == 0:
            sql = "INSERT INTO tblDailySummary (Year, Month, Day, DataIn, DataOut) VALUES "
            sql += "(%d, %d, %d, %d, %d)" % (YY, MM, DD, dataIn, dataOut )            
        else:
            sql = "UPDATE tblDailySummary SET DataIn=%d, DataOut=%d WHERE sumId=%d" % (dataIn, dataOut, id)
        self.conn.execute(sql)
        self.conn.commit()
        if id == 0:
            id = self._getLastInsertId()
        return id



    def closeConnection(self):
        self.dbConnect = False
        self.conn.close()


#    def writeData(self, dictData):

    def __init__(self, dbName):
        conn = sqlite3.connect(dbName)
        self.dbConnect = True
        self.conn = conn
        self._is_table_exists(self.conn)
#        print "Starting Init"

    def __del__(self):
        if (self.dbConnect == True):
            self.conn.close()
#        print "Done"


