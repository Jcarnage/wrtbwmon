#!/usr/bin/env python

import sqlite3
dbName = "netMonitor.sqlite"

# open the database
conn = sqlite3.connect(dbName)


# Read all the data that we want to modify
cur = conn.cursor()        
cur.execute("SELECT dataId, DataIn, DataOut FROM tblData WHERE dateId < 1088")
rows = cur.fetchall()
for row in rows:
    print "dataId: %s  DataIn: %10s  DataOut: %10s  Delta: %10s" % (row[0], row[1], row[2], (row[1]-row[2]))
    sql="UPDATE tblData SET DataIn=%d, DataOut=%d WHERE dataId=%d" %(row[2],row[1],row[0])
    print sql
#    conn.execute(sql)
#conn.commit()
conn.close()

