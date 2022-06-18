#*************************************************************
# Description: Shell Script for removing all QoS configurations on all 
#              ovs-vswitchdb switches.
# Filename   : stop-ovs-vsctl.sh
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py.
#*************************************************************
#!/bin/bash

sudo ovs-vsctl --all destroy qos
sudo ovs-vsctl --all destroy queue
sudo ovs-ofctl dump-ports-desc switch1
sudo ovs-ofctl dump-ports-desc switch2
sudo ovs-ofctl dump-ports-desc switch3