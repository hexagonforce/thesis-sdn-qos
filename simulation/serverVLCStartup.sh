#*************************************************************
# Description: Shell Script for Starting Up VLC telnet server process.
# Filename   : serverVLCStartup.sh
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py.
#*************************************************************
#!/bin/bash


echo "VLC Start: $(pwd)"
# iperf3 -s -p 5566 -i 1 &
sudo -u mininet nohup sh $(pwd)/run-vlc-server.sh &

pwd

(sleep 10; (sudo -u mininet nohup echo "Loading Config VLM $1" >> vlcstart.log; sudo -u mininet nohup python $(pwd)/telnetStartVLCServer.py $1)) & # ; 

exit 0