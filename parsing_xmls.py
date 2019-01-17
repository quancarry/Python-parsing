#!/usr/bin/env python

# export data sheets from lsx to csv
import pandas as pd
from pprint import pprint
import re
import os
import glob
import datetime 
import convert 
import shutil

os.chdir('/ftp/ftp_ericsson')
path_current=os.path.dirname(os.path.abspath(__file__))
if os.path.exists(path_current+'/MSC'):
	shutil.rmtree(path_current+'/MSC')
	shutil.rmtree(path_current+'/SMSC')
	shutil.rmtree(path_current+'/GGSN')
	shutil.rmtree(path_current+'/SGSN')
	shutil.rmtree(path_current+'/CRBT')
	
folder_file = glob.glob('*.xls')
os.makedirs(path_current+'/MSC')
os.makedirs(path_current+'/SMSC')
os.makedirs(path_current+'/GGSN')
os.makedirs(path_current+'/SGSN')
os.makedirs(path_current+'/CRBT')
def main(filename):
    xls = pd.ExcelFile(filename)
    if(re.match(r'^Billing',filename)):
        for ( i,sheet)in zip(range(len(xls.sheet_names)),xls.sheet_names):

            sheet_to_file=xls.parse(xls.sheet_names[i])
            str=sheet_to_file.to_string()
            if not os.path.exists(path_current+'/MSC_1'):
                os.makedirs(path_current+'/MSC_1')
            regex=re.search(r'([\d]+)',filename)
            with open ("MSC_1/"+sheet+"-"+regex.group(1)+".csv","w") as file:
                file.write(str)
                pass
            for fl in glob.glob(path_current+'/MSC/Start*'):
                        os.remove(fl)
            
    else:
        for ( i,sheet)in zip(range(len(xls.sheet_names)),xls.sheet_names):
            sheet_to_file=xls.parse(xls.sheet_names[i])
            str=sheet_to_file.to_string()
            #print str
            if (re.match(r'^CRBT',sheet)):
                if not os.path.exists(path_current+'/CRBT_1'):
                    os.makedirs(path_current+'/CRBT_1')
                with open ("CRBT_1/"+sheet+".csv","w") as file:
                    file.write(str)
                    pass
            elif(re.match(r'^GGSN',sheet)):
                if not os.path.exists(path_current+'/GGSN_1'):
                    os.makedirs(path_current+'/GGSN_1')
                with open ("GGSN_1/"+sheet+".csv","w") as file:
                    file.write(str)
                    pass
            elif(re.match(r'^SGSN',sheet)):
                if not os.path.exists(path_current+'/SGSN_1'):
                    os.makedirs(path_current+'/SGSN_1')
                with open ("SGSN_1/"+sheet+".csv","w") as file:
                    file.write(str)
                    pass
            elif(re.match(r'^SMSC',sheet)):
                if not os.path.exists(path_current+'/SMSC_1'):
                    os.makedirs(path_current+'/SMSC_1')
                with open ("SMSC_1/"+sheet+".csv","w") as file:
                    file.write(str)
                    pass
            else :
                print "regex not match !!"
            print "Separated completely ."
for filename in folder_file:
    
    if(re.match(r'^Billing',filename)):
        regex=re.search(r'([\d]+)',filename)
        
        yesterday=datetime.date.strftime(datetime.datetime.now() - datetime.timedelta(2), '%Y%m%d')
        
        if (regex.group(1)<yesterday):
            #main(filename)
            print "Date of files '"+filename+"' is end .Removing ..."
            os.remove(filename)
        else:
            print "Process Files ..."
            main(filename)
    else:
        print filename
        regex=re.search(r'([\d]+)',filename)
       
        yesterday=datetime.date.strftime(datetime.datetime.now() - datetime.timedelta(2), '%y%m%d')
       
        if (regex.group(1)<yesterday):
            #main(filename)
            print "Date of files '"+filename+"' is end . Removing ..."
            os.remove(filename)
        else :
            print "Process Files ..."
            main(filename)
def move_to_fd():
	dict=['MSC','SMSC','GGSN','SGSN','CRBT']
	
	for f in dict:
		os.chdir('/ftp/ftp_ericsson/'+f+'_1')
		folder_file2 = glob.glob('*.csv')

		for f2 in folder_file2:
			src = '/ftp/ftp_ericsson/'+f+'_1/'+f2
			dst = '/ftp/ftp_ericsson/'+f+'/'+f2
			shutil.move(src,dst)
convert.parsing()
move_to_fd()
os.rmdir(path_current+'/MSC_1')
os.rmdir(path_current+'/SMSC_1')
os.rmdir(path_current+'/SGSN_1')
os.rmdir(path_current+'/GGSN_1')
os.rmdir(path_current+'/CRBT_1')
