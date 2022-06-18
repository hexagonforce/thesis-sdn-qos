#*************************************************************
# Description: Shell Script for Starting Up VLC server client process on 
#              each client host based on content quality.
# Filename   : run-client-vlc-tests.sh
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py.
#*************************************************************
#!/bin/bash

echo "RUNNING CLIENT VLC TESTS" >> vlc_tests.log

clientname=`hostname -I`
hostname=`hostname -I`
exectype="medium"
startingport=4313
datetimestr=`date +%m%d%Y%H%M%S`
usecase=0

count=0
sleeptime=240

hostname=`echo $hostname| tr -d '[[:space:]]'`

if [ $# -gt 0 ]; then
	clientname=$1
fi

if [ $# -gt 1 ]; then
	exectype=$2
fi

if [ $# -gt 2 ]; then
    datetimestr=$3
fi

if [ $# -gt 3 ]; then
    usecase=$4
fi

if [ $# -gt 4 ]; then
    startingport=$5
fi

cd /home/ubuntu/thesis/SDNQoS/Load_Generation

for i in `seq 0 $count`;
do
	portToUse=$(($startingport + $i))
	echo "EXECTYPE:"$exectype >> vlc_tests.log
	echo "portToUse:" $portToUse "clientname:" $clientname "datetimestr:" $datetimestr "usecase:" $usecase >> vlc_tests.log
	python /home/ubuntu/thesis/Tests/bash_str_comp.py  $exectype "medium"

	if  [ "$exectype" == medium ]; then
		echo "RUNNING MEDIUM" >> vlc_tests.log
		sh run-vlc-client-medium.sh $portToUse $clientname $datetimestr $usecase &
	elif [ "$exectype" == high ]; then
		echo "RUNNING HIGH" >> vlc_tests.log
		sh run-vlc-client-high.sh $portToUse  $clientname $datetimestr $usecase &
	else
		echo "NONE MATCHED" >> vlc_tests.log
	fi
done 
exit 0
