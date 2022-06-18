#*************************************************************
# Description: Shell Script for Starting Up VLC telnet client process on 
#              each client host.
# Filename   : run-client-vlc-telnet-tests.sh
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py.
#*************************************************************
#!/bin/bash

clientname=`hostname -I`
hostname=`hostname -I`
exectype="medium"
startingport=4313
datetimestr=`date +%m%d%Y%H%M%S`
usecase=0
endtimestr=`date +%m%d%Y%H%M%S`
queuecase='0.0'
loadcase=0

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
    endtimestr=$5
fi

if [ $# -gt 5 ]; then
    startingport=$6
fi

if [ $# -gt 6 ]; then
    queuecase=$7
fi

if [ $# -gt 7 ]; then
    loadcase=$8
fi


for i in `seq 0 $count`;
do
    portToUse=$(($startingport + $i))
    echo $portToUse $clientname $datetimestr $exectype $hostname $usecase $queuecase $loadcase $endtimest >> vlctelnettest.log
    python $(pwd)/scripts/custom/simulation/vlcrctelnetclient.py -p $portToUse -c $clientname -s $9 -d $datetimestr -t $exectype -h $hostname -u $usecase -q $queuecase -l $loadcase -e $endtimestr &  
done 
exit 0