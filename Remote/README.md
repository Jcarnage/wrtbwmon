# REMOTE
Updated features to code originally pulled from https://code.google.com/p/wrtbwmon/.

## New features
	- Uses sql on a remote device to capture and display traffic data
	- Requires updated netMon.awk script and modified wrtbwmon.sh


### What does it do?
`wrtbwmon` was designed to track bandwidth consumption on home routers. 
Using UDP and sqlite a remote *nix device can be used to capture data sent from 
the router (using UDP) for long term analysis and trend calculations

### How do I use it?
- Please read the instructions on installing wrtbwmon on your router (first)
- Review install.sh and update to match your system configuration
- Install: sudo ./install
- launch receiver from the Remote directory :  ./monitor.py &
- view usage graphs by connecting to your *nix device using a webrowser:
	ex:   http://mydevice/cgi-bin/dailyReport.py
		  http://mydevice/cgi-bin/deviceDailyReport.py
		  http://mydevice/cgi-bin/monthlyReport.py

### Regular updates
 - Add the following to user's crontab, assuming `<script location>` is replaced with the actual location:
	5 0 * * * /<script location>/nightly.sh


