import time
import datetime

##########################################################################
# last_day_of_month borrowed from: 
#http://stackoverflow.com/questions/42950/get-last-day-of-the-month-in-python
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4) 
    return next_month - datetime.timedelta(days=next_month.day)

#
# Given the Year (YYYY) and Month (MM) returns the total number of days 
# in that month for that year.   Takes care of leap years
def getDaysInMonth(YY, MM):
    return last_day_of_month(datetime.date(YY, MM, 1)).day

##########################################################################
def getDateToday():
    myDate = time.localtime()
    return (myDate.tm_year, myDate.tm_mon, myDate.tm_mday)  

##########################################################################
def getDateYesterday():
    myDate = datetime.date.today() - datetime.timedelta(1)
    return (myDate.year, myDate.month, myDate.day)  

##########################################################################
def yesterday(YY, MM, DD):
    newDay = datetime.date(YY,MM,DD) - datetime.timedelta(days=1)
    return (str(newDay.year),str(newDay.month), str(newDay.day))

##########################################################################
def tomorrow(YY, MM, DD):     
    newDay = datetime.date(YY,MM,DD) + datetime.timedelta(days=1)
    return (str(newDay.year),str(newDay.month), str(newDay.day))

##########################################################################
def lastMonth(YY, MM):
    if MM == 1:
        MM == 12
        YY -= 1
    else:
        MM -= 1
    return (YY, MM)

##########################################################################
def nextMonth(YY, MM):
    if MM == 12:
        MM = 1
        YY += 1
    else:
        MM += 1
    return (YY, MM)
