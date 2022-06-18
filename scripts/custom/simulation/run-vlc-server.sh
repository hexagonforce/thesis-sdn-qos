#*************************************************************
# Description: Shell Script for Starting Up VLC server process.
# Filename   : run-vlc-server.sh
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py.
#*************************************************************
#!/bin/bash

vlcslogfilename="$(pwd)/test.results/vlc-server/results.run-vlc-server-`hostname -I`.`date +%m%d%Y%H%M%S`.log"
vlcslogfilename=`echo $vlcslogfilename| tr -d '[[:space:]]'`

vlc -vvv --file-logging --logfile=$vlcslogfilename --stats --color -I telnet --telnet-password ubuntu --rtsp-port 5004 --rtsp-throttle-users 0 --network-caching=200000 --file-caching=200000 

exit 0