#!/usr/bin/env python

import unittest,sys

sys.path.append('../')

from netMonRcv import *

class test_netmonrcv(unittest.TestCase):

    logger = None

    def tearDown(self):
        macList.clear()

    def test_splitData(self):
        netMon = NetMonitor(self.logger)
        values = ["00:0C:29:E5:4C:A2", 360, 12560]
        self.assertEqual(netMon.splitData("00:0C:29:E5:4C:A2,360,12560"), values)

    def test_splitDataFail(self):
        netMon = NetMonitor(self.logger)      
        self.assertEqual(netMon.splitData("00:0C:29:E5:4C:A2,360,"), None)

    def test_splitData(self):
        netMon = NetMonitor(self.logger)
        self.assertEqual(netMon.splitData(""), None)
        
    def test_addToDict(self):
        netMon = NetMonitor(self.logger)
        value = ["00:0C:29:E5:4C:A2", 360, 12560]
        netMon.addToDict(value)
        self.assertEqual(macList["00:0C:29:E5:4C:A2"],[360,12560]) 

    def test_updateDictFail(self):
        netMon = NetMonitor(self.logger)
        value = ["00:0C:29:E5:4C:A2", 360]
        netMon.addToDict(value)
        self.assertEqual(len(macList), 0)
        value = ["00:0C:29:E5:4C:A2", 360, 150, 1501]
        netMon.addToDict(value)
        self.assertEqual(len(macList), 0)

    def tests_updateDict(self):
        netMon = NetMonitor(self.logger)
        value = ["00:0C:29:E5:4C:A2", 360, 12560]
        netMon.addToDict(value)
        netMon.addToDict(value)
        self.assertEqual(macList["00:0C:29:E5:4C:A2"],[720,25120])

    def test_updateDictMultValues(self):
        netMon = NetMonitor(self.logger)
        value = ["00:0C:29:E5:4C:A2", 360, 12560]
        netMon.addToDict(value)
        netMon.addToDict(value)
        value = ["00:0C:29:E5:4C:A3", 360, 12560]
        netMon.addToDict(value)
        self.assertEqual(len(macList),2)
        self.assertEqual(macList["00:0C:29:E5:4C:A2"],[720,25120]) 
        self.assertEqual(macList["00:0C:29:E5:4C:A3"],[360,12560])

    def test_parseData(self):
        netMon = NetMonitor(self.logger)
        value = "00:0C:29:E5:4C:A2,362,12561\n10:22:33:44:AA:BB,360,12560\n\n"
        netMon.parseData(value)
        self.assertEqual(len(macList),2)
        self.assertEqual(macList["00:0C:29:E5:4C:A2"],[362,12561]) 
        self.assertEqual(macList["10:22:33:44:AA:BB"],[360,12560]) 

    def test_parseDataList(self):
        netMon = NetMonitor(self.logger) 
        value = ['b8:27:eb:f2:e0:33,28132,47167\n94:de:80:ac:19:5e,50715,1028493\n10:1c:0c:44:ca:9d,404,591\nb4:ae:2b:67:62:ca,2945161,22555608\n3c:a9:f4:38:76:0c,1654860,7959085\nc0:1a:da:c0:36:c9,1324,521\n']
        netMon.parseData(value, False)
        self.assertEqual(len(macList),6)
        self.assertEqual(macList["b8:27:eb:f2:e0:33"],[28132,47167]) 
        self.assertEqual(macList["b4:ae:2b:67:62:ca"],[2945161,22555608])
        
    def test_parseDataMulitItemList(self):
        netMon = NetMonitor(self.logger) 
        value = ['b8:27:eb:f2:e0:33,28132,47167\n','94:de:80:ac:19:5e,50715,1028493\n','10:1c:0c:44:ca:9d,404,591\n','b4:ae:2b:67:62:ca,2945161,22555608\n','3c:a9:f4:38:76:0c,1654860,7959085\n','c0:1a:da:c0:36:c9,1324,521\n']
        netMon.parseData(value, False)
        self.assertEqual(len(macList),6)
        self.assertEqual(macList["b8:27:eb:f2:e0:33"],[28132,47167]) 
        self.assertEqual(macList["b4:ae:2b:67:62:ca"],[2945161,22555608])
     

if __name__ == '__main__':
    unittest.main()
