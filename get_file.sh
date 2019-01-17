#bin/bash

cd /ftp

HOST=10.10.194.3
# USER=hlrftp1
# PASSWORD=Ericsson@123

USER=hlrftp2
PASSWORD=Vietnam@123

DATE=`date -d yesterday +%Y%m`
#DATE="20180215"

DATE_HLR=`date +%b`
echo "$DATE Connect to FTP to get files."
ftp -inv $HOST <<EOF
user $USER $PASSWORD
binary
cd /home/hlrftp
ls -al
mget "UDC Dump *$DATE_HLR*"
#mget "VAS Dump $DATE*"

bye
EOF

for f in *

do
	echo $f
	echo "--------"
	if [[ $f =~ ^UDC.*\.zip$ ]];
	then
				echo "Unzip $f"
                unzip  -j /ftp/"$f" -d /ftp/ftp_hlr/HLR_DUMP/"$f"
                echo "Removing file - $f"
                rm -rf /ftp/"$f"

	elif [[ $f =~ ^VAS.*\.zip$ ]];
	then
				echo "Unzip $f"
				unzip -j "$f" -d /ftp/ftp_hlr/VAS_DUMP/
				echo "Removing file - $f"
				rm -rf /ftp/"$f"
	
	else
		echo "Ignore $f"
	fi
done

cd /ftp/ftp_hlr/VAS_DUMP
	for f in *
	do 
	
	if [[ $f =~ ^CRBT.zip$ ]];
	then
		unzip -j "$f"
		echo "Unzip $f"
		rm -rf /ftp/ftp_hlr/VAS_DUMP/"$f"
		echo "Removing file - $f"
	elif [[ $f =~ ^MOIP.zip$ ]];
	then
			echo " Wait for Unzip $f"
	else 
		echo "Ignore $f"
	fi
	done
	
	for f in *
	do
	if [ -d "$f" ] ; 
	then
		echo "$f is a directory";
	
	elif [[ $f =~ ^crbt_.*\.gz$ ]];
	then
		gunzip  "$f"
		echo "Gunzip $f"
		
	elif [[ $f =~ ^ActiveUsers* ]];
	then
		echo "Moving $f to MOIP/"
		mv "$f" MOIP/"$f""_$DATE"
		
	elif [[ $f =~ ^.*.zip$ ]];
	then
		echo "Ignore $f"
	else 
		echo "Moving $f to MOIP/"
		mv "$f" MOIP/
	fi
	
	done
	for f in *
	do
	if [ -d "$f" ] ; 
	then
		echo "$f is a directory";
	
	elif [[ $f =~ ^crbt_* ]];
	then
		echo "Moving $f to CRBT/"
		mv "$f" CRBT/
		
	else
		echo "Unzip $f"
		unzip -j "$f" -d /ftp/ftp_hlr/VAS_DUMP
		echo "Removing file - $f"
		rm -rf /ftp/ftp_hlr/VAS_DUMP/"$f"
		
		
	fi
	done
	
	for f in *
	do
	if [ -d "$f" ] ; 
	then
		echo "$f is a directory";
		
	elif [[ $f =~ ^ActiveUsers* ]];
	then 
		echo "Moving $f to MOIP/"
		 mv "$f" MOIP/"$f""_$DATE"
	else 
		echo "Moving $f to MOIP/"
		mv "$f" MOIP/"$f"
	fi 
	done
