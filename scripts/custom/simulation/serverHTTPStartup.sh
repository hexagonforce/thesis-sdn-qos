#*************************************************************
# Description: Shell Script for Starting Up Apache server process.
# Filename   : serverHTTPStartup.sh
# Author     : O. V. Chato
# Execution  : To be called by executeTest.py.
#*************************************************************
#!/bin/bash

cd /home/ubuntu/thesis/SDNQoS/Load-Generation

sudo /etc/init.d/apache2 status >> Logs_http/http_startup.log
sudo /etc/init.d/apache2 start Logs_http/http_startup.log
sudo /etc/init.d/apache2 status >> Logs_http/http_startup.log

exit 0
