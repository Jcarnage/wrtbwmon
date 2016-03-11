#!/bin/bash

srcDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


# The following is the title that will appear on all the web pages
pageTitles="Enter the Title for the Web Pages"

# *****************************************************************
# The following section will identify the location of cgi-bin based
# on commonly known locations
# *****************************************************************
echo Copying Python files into the CGI-BIN directory
# ********  Identify location of cgi-bin
if [ -d "/usr/lib/cgi-bin" ] ; then
    CgiBin=/usr/lib/cgi-bin
elif [ -d "/var/www/cgi-bin" ] ; then
    CgiBin=/var/www/cgi-bin
else
    echo "ERROR: Unknown system - can't find cgi-bin"
    exit
fi

# *****************************************************************
# The following section will copy and update the python files used
# for serving up the live web pages
# *****************************************************************
pythonFiles=(dailyReport.py deviceDailyReport.py monthlyReport.py dailyBwReport.py)
for file in "${pythonFiles[@]}"
  do
	sed s/PAGE_TITLE/"$pageTitles"/ $file > $CgiBin/$file
    chmod +x $CgiBin/$file 
  done


# *****************************************************************
#  Create the symbolic link (if necessary).  This gives the python
#  scripts in the cgi-bin directory easy access to the relevant 
#  python support scripts and database file
# *****************************************************************
if [ ! -L "$CgiBin/data" ]; then 
	echo "Creating Sympbolic Link"
	ln -s $srcDir $CgiBin/data 
fi

# *****************************************************************
# Identify the location of our html directory
# *****************************************************************
if [ -d "/var/www/html" ] ; then
    htmlPath=/var/www/html/netMonitor
elif [ -d "/var/www/" ] ; then
    htmlPath=/var/www/netMonitor
else
    echo "ERROR: Unknown system - can't find html path"
    exit
fi

# *****************************************************************
# Create our html subdirectory (if it does not exist) before 
# copying any of our relevant html/css files over
# *****************************************************************
echo Copying HTML/CCS files
if [ ! -d "$htmlPath" ] ; then
	echo "Creating path for HTML/CSS files"
	mkdir -p $htmlPath
fi

cp stylesheet.css $htmlPath/.


