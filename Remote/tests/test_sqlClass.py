#!/usr/bin/env python


import unittest
import os,sys 
sys.path.append('../')
import sqlClass

dbName = "test.sqlite"
macList = {}

def buildDatabase():
    try:
        os.remove(dbName)
    except:
        pass

class tstSqlClass(unittest.TestCase):
    # Some tests must occur before others.  We use the _a_, _b_, etc. in the test name to
    # put an order to our tests (they are alphabetical)
    def test_Close(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.dbConnect, True)
        q.closeConnection()
        self.assertEqual(q.dbConnect, False)

    def test_a_writeMac(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q._writeMac("00:11:22:33:FF:EE","macMini"),1)
        q.closeConnection()  

    def test_a_writeMacDuplicate(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q._writeMac("00:11:22:33:FF:EE","macMini"),1)
        q.closeConnection()      

    def test_a_writeDate(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q._writeDate(2016,2,20,10,59,1021),1)
        self.assertEqual(q._getLastDateId(),1)
        q.closeConnection() 

    def test_a_getSummaryId(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.getDailySummaryId(2016,2,23), 0)

    def test_a_updateDailySummary(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.updateDailySummary(2016,2,23,10000, 30000), 1)
        self.assertEqual(q.updateDailySummary(2016,2,24,20000, 50000), 2)
        self.assertEqual(q.updateDailySummary(2016,2,23,15000, 30050), 1)

    def test_b_getSummaryId(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.getDailySummaryId(2016,2,23), 1)

    def test_b_returnMonthlySummary(self):
        q = sqlClass.sqlAccess("test.sqlite")
        items = q.returnMonthlySummary(2016 ,2)
        self.assertEqual(2, len(items))

    def test_b_timeStamp(self):
        q = sqlClass.sqlAccess("test.sqlite")
        (r1, r2, r3, r4, r5) = q._timeStamp(1000)
        self.assertEqual(r1, 1969)
        self.assertEqual(r2, 12)
        self.assertEqual(r3, 31)
        self.assertEqual(r4, 19)
        self.assertEqual(r5, 16)

    def test_b_timeStamp(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q._timeStamp(), 2)
        self.assertEqual(q._getLastDateId(),2)

    def test_b_timeStampGet(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q._getDateId(2016,2,20,10,59),1)

    def test_c_getDateRange(self):
        q = sqlClass.sqlAccess("test.sqlite")
        q._writeDate(2016,2,21,10,59,1020)
        q._writeDate(2016,2,22,10,59,2021)
        q._writeDate(2016,2,23,10,59,3022)
        q._writeDate(2016,2,23,11,02,5023)
        q._writeDate(2016,2,24,10,59,6024)
        q._writeDate(2016,4,2,10,59,7021)
        self.assertEqual(q._getDayRange(2017,3,24), (0,0))
        self.assertEqual(q._getDayRange(2016,2,23),(5,6))

    def test_b_getMacId(self):
        q = sqlClass.sqlAccess("test.sqlite")
        r = q._getMacId("00:11:22:33:FF:EE")
        self.assertEqual(r,1)
        
    def test_b_getDeviceList(self):
        q = sqlClass.sqlAccess("test.sqlite")
        # Put some random macId's in the database
        q._writeMac("00:11:22:33:10:EE","Device2")
        q._writeMac("00:11:22:33:11:EE","Device3")
        q._writeMac("00:11:22:33:12:EE","Device4")
        dictNames = q.getDeviceList()
        self.assertEqual(len(dictNames), 4)

    def test_b_getDeviceNames(self):
        q = sqlClass.sqlAccess("test.sqlite")
        deviceNames = q.getAllDeviceNames()
        self.assertEqual(len(deviceNames), 4)
        self.assertEqual(deviceNames[0], "macMini")
        self.assertEqual(deviceNames[1], "Device2")
        self.assertEqual(deviceNames[2], "Device3")
        self.assertEqual(deviceNames[3], "Device4")       
        
    def test_b_storeEmptyData(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.storeData(macList), -1)

    def test_c_storeData(self):
        macList["00:11:22:33:44:55"] = [500, 1200];
        macList["01:12:23:34:45:56"] = [1500, 12200];
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.storeData(macList), 1)

    def test_d_returnDayValues(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.returnDayValues(2017,15,1,True),None)
        
    def test_d_returnDeviceDailyInfoValues(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.returnDeviceDailyInfo(2017,15,1,2),None)

#    def test_d_returnMonthlySummary(self):
#        q = sqlClass.sqlAccess("test.sqlite")
#        values = q.returnMonthlySummary(2016,2)
#        print values

    def test_d_getRecordingIntervals(self):
        q = sqlClass.sqlAccess("test.sqlite")
        values = q.getRecordingIntervals(2016,2,23)
        self.assertEqual(values[0], "19:50")
        self.assertEqual(values[1], "20:23")

    def test_d_returnMonthValues(self):
        q = sqlClass.sqlAccess("test.sqlite")
        self.assertEqual(q.returnMonthValues(2017,15,True),None)
        self.assertEqual(q.returnMonthValues(2016,4,True),None)


if __name__ == '__main__':
    buildDatabase()
    unittest.main()
