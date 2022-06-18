#*************************************************************
# Description: Shell Script for executing VLC server client commands on 
#              each client host for high content quality.
# Filename   : run-vlc-client-high.sh
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py.
#*************************************************************
#!/bin/bash

cd /home/ubuntu/thesis/SDNQoS/Load_Generation
sudo -u ubuntu nohup echo "RUNNING CLIENT VLC HIGH" >> high.log

portToUse=4313
aboutputdir="/home/ubuntu/SDNQoS/test.results"
iperf3_logs="iperf3_logs"
datetimestr=`date +%m%d%Y%H%M%S`
clientname=`hostname -I`
hostname=`hostname -I`
usecase=0

if [ $# -gt 0 ]; then
	portToUse=$1
fi

if [ $# -gt 1 ]; then
	clientname=$2
fi

if [ $# -gt 2 ]; then
	datetimestr=$3
fi

if [ $# -gt 3 ]; then
    usecase=$4
fi

if [ $# -gt 4 ]; then
    aboutputdir=$5
fi

if [ $# -gt 5 ]; then
    iperf3_logs=$6
fi

vlcclogfilename="$(pwd)/test.results/$datetimestr-case$usecase/logs/run-vlc-client-high-$portToUse-$clientname.$datetimestr.log"
vlcclogfilename=`echo $vlcclogfilename| tr -d '[[:space:]]'`
hostname=`echo $hostname| tr -d '[[:space:]]'`

cd "${datetimestr}-case${usecase}/logs" >> ab_test_pwd.log

echo $hostname $portToUse >> high.log
cvlc -vvv --file-logging --logfile=$vlcslogfilename --intf rc --rc-host=$hostname:$portToUse -Vdummy --noaudio --novideo --rc-fake-tty --no-sout-display-video --no-sout-display-audio --no-playlist-autostart --no-video-deco --no-embedded-video --input-repeat=5 --quiet rtsp://10.0.1.104:5004/PurlHigh &

exit 0
