from datetime import datetime, timedelta
from ftplib import FTP
from dateutil import parser
import os
import shutil
import re
os.chdir("/splunk_data/TAP/TAP_ENCODE")

path_dist='/splunk_data/TAP'

if os.path.exists(path_dist+'/TAP_ENCODE'):
	shutil.rmtree(path_dist+'/TAP_ENCODE')		
	os.makedirs(path_dist+'/TAP_ENCODE')

os.chdir("/splunk_data/TAP/TAP_ENCODE")	

ftp = FTP("10.6.3.68")
ftp.login("sv8_tap_ftp","sv8tapftp@2018")

lines = []
# ftp.dir("/svw/svprod/data/server/roaming/roaming/input/tap/", lines.append) 
# directory="/svw/svprod/data/server/roaming/roaming/input/tap/" 

ftp.dir("/svw/svprod/data/server/roaming/roaming/archive/tap/", lines.append) 
directory="/svw/svprod/data/server/roaming/roaming/archive/tap/" 

#"/svw/svprod/data/server/roaming/roaming/archive/tap/"

ftp.cwd(directory)
for line in lines:
	tokens = line.split()
	name = tokens[8]
	time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
	time = parser.parse(time_str)
	# print time

	yesterday = datetime.now() - timedelta(days=1)
	date=str(yesterday.strftime('%Y-%m-%d'))
	# print str(time)
	# print date
	if	date in str(time):
		if "CD" in name:
			fhandle = open(name, 'wb')
			print 'Getting ' + name #for confort sake, shows the file that's being retrieved
			ftp.retrbinary('RETR ' + name, fhandle.write)
			fhandle.close()
ftp.close()

ftp = FTP("10.8.7.17")
ftp.login("jautotap","SftpTap2018")

lines = []
ftp.dir("/data/CB/server/roaming/archive/tap/", lines.append)
directory="/data/CB/server/roaming/archive/tap/"
ftp.cwd(directory)

for line2 in lines:

	tokens = line2.split()
	try:
		name = tokens[8]
		time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
		time = parser.parse(time_str)
		yesterday = datetime.now() - timedelta(days=12)
		date=str(yesterday.strftime('%Y-%m-%d'))
	print str(time)
	print date
		if	date in str(time):
			if "CDVNM" in name:
				fhandle = open(name, 'wb')
				print 'Getting ' + name #for confort sake, shows the file that's being retrieved
				ftp.retrbinary('RETR ' + name, fhandle.write)
				fhandle.close()
			
	except IndexError:
		continue
ftp.close()
