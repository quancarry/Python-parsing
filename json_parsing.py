# -*- coding: utf-8 -*-
#!/bin/sh
# Script running to parsing as flow:
# CDR TapIn,TapOut -> TAP3Editor ->Json parsing->
# Classification SMS MT,Call MT and GGSN .

# -----------------------
# Module for explore folder and file.
import shutil
# Module for regular expression.
import re
# Module for parsing json. To reach Object and value.
import json
# Module for Opreation SystemError
import os

from time import gmtime, strftime
# -----------------------
os.chdir("/splunk_data/TAP/TAP_DECODE")	

path_dist=['TAPIN','TAPOUT']

for path_seq in path_dist:
	path_current='/splunk_data/'+path_seq
	if os.path.exists(path_current+'/GGSN'):
		shutil.rmtree(path_current+'/GGSN')
		shutil.rmtree(path_current+'/MT')
		shutil.rmtree(path_current+'/MO')
	os.makedirs(path_current+'/GGSN')
	os.makedirs(path_current+'/MT')
	os.makedirs(path_current+'/MO')


# Path which store TapIn,TapOut decoded. 
path = '/splunk_data/TAP/TAP_DECODE'
# Change dir
#os.chdir("/splunk_data/TAP/TAP_DECODE")
# Read all file in folder for process :
for filename in os.listdir(path):
	if "CD" in filename:
		print filename
		if os.path.getsize(filename)>1332:
			print "Processing File : "+filename
			with open(filename) as f:
				i=0
				g=0
				h=0
				a=[]
				a=f.read()
				# Repalce "=>" to ":" Json format.
				replaced = re.sub('=>', ':',a)
				# Clear first line.
				replaced2 = re.sub('\$VAR\d\s\=', '',replaced)
				# Remove unstructure json character.
				replaced3 = re.sub('\;$','',replaced2)
				# Repalce Escape character
				# Remove unstructure json character.
				# Remove unstructure json character.
				# Remove unstructure json character.
				replaced4 = re.sub('\"chargingId\".*\s+.*value.*\s+','"chargingId" : "',replaced3)
				replaced5 = re.sub('\,\s+\d\s+.*\s+.*sign.*\s+.*Math.*\)','"',replaced4)
				replaced6 = replaced5.replace('\\\"\\','')

				replaced7 = replaced6.replace('\\','')
				replaced8 = replaced7.replace('\/','')
				
				replaced9 = replaced8.replace('\@','')
				replaced10 = replaced9.replace('\)','')
				replaced11 = replaced10.replace(';',',')
				replaced12 = re.sub('\"callReference\"\s\:\s\".*\"\,','"callReference" : "Encoded String",',replaced11)
				# Load json structure.
				#print replaced11
				if filename=='CDISRK5VNMVM01597':
					with open("a.txt","w") as f:
						f.write(replaced12)
				j=json.loads(replaced12)
			   
				# Read Object and element
				if 'transferBatch' in j:
					for dist in j['transferBatch']['callEventDetails']:
						if 'gprsCall' in dist:
							i=i+1
							cond=re.search('^CDVNM*',filename)
							if cond:
								with open("/splunk_data/TAPOUT/GGSN/GGSN_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
									if i==1:
									   
										 f2.write(json.dumps(dist, indent=4))
									else:
										
										 f2.write(json.dumps(dist, indent=4))
									f2.close()
							else:
								with open("/splunk_data/TAPIN/GGSN/GGSN_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
									if i==1:
									   
										 f2.write(json.dumps(dist, indent=4))
									else:
										
										 f2.write(json.dumps(dist, indent=4))
									f2.close()
						elif 'mobileTerminatedCall' in dist:
							# In Object 'mobileTerminatedCall' got two type of CDR : 
							# SMS MT and Call MT with same structure , but value 
							# ChargedItem represent for Type .
							for list2 in dist['mobileTerminatedCall']['basicServiceUsedList']:
								for list3 in list2['chargeInformationList']:
									if list3['chargedItem']=='E':
										g=g+1
										cond=re.search('^CDVNM*',filename)
										if cond:
											with open("/splunk_data/TAPOUT/MT/SMSMT_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
												if g==1:
												   f2.write(json.dumps(dist, indent=4))
												else:
						
												   f2.write(json.dumps(dist, indent=4))
												f2.close()
										else:
											with open("/splunk_data/TAPIN/MT/SMSMT_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
												if g==1:
												   f2.write(json.dumps(dist, indent=4))
												else:
						
												   f2.write(json.dumps(dist, indent=4))
												f2.close()
									elif list3['chargedItem']=='D':
										h=h+1
										cond=re.search('^CDVNM*',filename)
										if cond:
											with open("/splunk_data/TAPOUT/MT/MSCMT_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
												if h==1:
													
													 f2.write(json.dumps(dist, indent=4))
												else:
												   
													 f2.write(json.dumps(dist, indent=4))
												f2.close()
										else:
												with open("/splunk_data/TAPIN/MT/MSCMT_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
													if h==1:
														
														 f2.write(json.dumps(dist, indent=4))
													else:
													   
														 f2.write(json.dumps(dist, indent=4))
													f2.close()
						else:
							for list2 in dist['mobileOriginatedCall']['basicServiceUsedList']:
								for list3 in list2['chargeInformationList']:
									if list3['chargedItem']=='E':
										g=g+1
										cond=re.search('^CDVNM*',filename)
										if cond:
											with open("/splunk_data/TAPOUT/MO/SMSMO_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
												if g==1:
												   f2.write(json.dumps(dist, indent=4))
												else:
						
												   f2.write(json.dumps(dist, indent=4))
												f2.close()
										else:
											with open("/splunk_data/TAPIN/MO/SMSMO_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
												if g==1:
												   f2.write(json.dumps(dist, indent=4))
												else:
						
												   f2.write(json.dumps(dist, indent=4))
												f2.close()
									elif list3['chargedItem']=='D':
										h=h+1
										cond=re.search('^CDVNM*',filename)
										if cond:
											with open("/splunk_data/TAPOUT/MO/MSCMO_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
												if h==1:
													
													 f2.write(json.dumps(dist, indent=4))
												else:
												   
													 f2.write(json.dumps(dist, indent=4))
												f2.close()
										else:
											with open("/splunk_data/TAPIN/MO/MSCMO_"+filename+"_"+str(strftime("%Y%m%d%H%M%S", gmtime())),"a") as f2:
												if h==1:
													
													 f2.write(json.dumps(dist, indent=4))
												else:
												   
													 f2.write(json.dumps(dist, indent=4))
												f2.close()
		else:
			continue
	else:
		continue

	print 'Total GGSN record :'+str(i)
	print 'Total SMS MT record :'+str(g)
	print 'Total Call MT record :'+str(h)
