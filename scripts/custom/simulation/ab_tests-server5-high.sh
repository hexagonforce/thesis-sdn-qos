#!/bin/bash

pwd
difference=0
aboutputfile="$(pwd)/scripts/custom"
execdir="$(pwd)/scripts/custom"
aboutputdir="$(pwd)/test.results"
iperf3_logs="iperf3_logs"
hostname=`hostname -I`
datetimestr=`date +%m%d%Y%H%M%S`
usecase=0
aboutputfile2="/home/ubuntu/thesis/SDNQoS/Load_Generation"
queuecase='0.0'
loadcase=0

hostname=`echo $hostname| tr -d '[[:space:]]'`

if [ $# -gt  0 ]; then
	difference=$1
fi

if [ $# -gt 1 ]; then
	aboutputfile=$2
fi

if [ $# -gt 2 ]; then
	execdir=$3
fi

if [ $# -gt 3 ]; then
    hostname=$4
fi

if [ $# -gt 4 ]; then
    datetimestr=$5
fi

if [ $# -gt 5 ]; then
    usecase=$6
fi

if [ $# -gt 6 ]; then
    aboutputdir=$7
fi

if [ $# -gt 7 ]; then
    queuecase=$8
fi

if [ $# -gt 8 ]; then
    loadcase=$9
fi

if [ $# -gt 9 ]; then
    iperf3_logs=$10
fi

cd "${datetimestr}-case${usecase}/logs" >> ab_test_pwd.log
pwd >> ab_test_pwd.log

echo "difference: " $1 "aboutputfile: "$aboutputfile "execdir: " $execdir "hostname: " "aboutputdir: " $aboutputdir>> ab_test.log
# iperf3 -c 10.0.1.105 -p 5566 -t 4313 > $iperf3_logs &
sudo -u ubuntu ab -l -r -n 50000 -c 10 -k -t $1 -s 240 -q -H "Accept-Encoding: gzip, deflate" http://10.0.1.105/1GB.bin > $aboutputdir/$aboutputfile &





