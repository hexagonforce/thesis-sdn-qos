#*************************************************************
# Description: Shell Script for Starting Up ifstat client process on 
#              each client host. Additionally, commands to stop
#              ifstat, VLC, and Apache server processes as well as
#              removing all QoS configurations on all ovs-vswitchdb
#              switches have been piggy-backed here as the completion
#              of ifstat also signals completion of the test.
# Filename   : run-ipstat.sh
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py.
#*************************************************************
#!/bin/bash

usecase=0
queuecase="1.0"
loadcase=1
sleeptime=330

if [ $# -gt 0 ]; then
    usecase=$1
fi

if [ $# -gt 1 ]; then
    queuecase=$2
fi

if [ $# -gt 2 ]; then
    loadcase=$3
fi

if [ $# -gt 3 ]; then
    sleeptime=$4
fi

cd /home/ubuntu/thesis/SDNQoS/

sudo -u ubuntu ifstat -i switch7-eth3 -t -n > /home/ubuntu/thesis/SDNQoS/test.results/ifstat-results-$usecase-$loadcase-$queuecase.csv &

sleep $sleeptime;

serversleeptime=$((sleeptime + 20))

sudo pkill -f ifstat &
# (sleep $serversleeptime; (sudo -u ubuntu nohup echo "Killing VLC Server Process"; sudo nohup pkill -f vlc)) &

# (sleep $serversleeptime; (sudo -u ubuntu nohup echo "Stopping HTTPD and Killing apache2 Server Process"; sudo nohup /etc/init.d/apache2 stop; sudo nohup pkill -f apache2)) &

# (sleep $serversleeptime; (sudo -u ubuntu nohup echo "Clearing QoS"; sudo /home/ubuntu/thesis/SDNQoS/Load_Generation/stop-ovs-vsctl.sh)) &

exit 0