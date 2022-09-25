import csv
import subprocess
import os
from pathlib import Path
import yaml
from datetime import datetime
import time

BASEDIR = os.getcwd()
ABTESTS_DIR = f'{BASEDIR}/simulation/test.results/ab-tests'
def run(net, serverdata, loadconfig):
    for loadrow in loadconfig:
        clientname = loadrow[0]
        httpload = loadrow[1].split('-')
        loadtype = httpload[1]

        servernum = int(httpload[2])
        servername = f'server{servernum}'
        currserverdata = serverdata[servername]

        file = currserverdata[loadtype]
        host = net.getNodeByName(clientname)
        server = net.getNodeByName(servername)

        cmd = (
            'sudo -u mininet ab -l -r -n 50000 -c 10 -k -t 300 -s 300 '
            f'-q -H "Accept-Encoding: gzip, deflate" http://{server.IP()}/{file} > '
            f'{ABTESTS_DIR}/{clientname}-{servername}-{loadtype}.ab.txt &' 
        )
        cmd2 = (
            'sudo -u mininet wrk --header "Accept-Encoding: gzip, deflate" -c 10 '
            f'-d 300 --timeout 300 http://{server.IP()}/{file} > '
            f'{ABTESTS_DIR}/{clientname}-{servername}-{loadtype}.wrk.txt 2> /dev/null &'
        )
        cmd3 = (
            'sudo -u mininet hey -A "Accept-Encoding: gzip, deflate" -c 10 '
            f'-z 300s -t 300 \'http://{server.IP()}/{file}\' > '
            f'{ABTESTS_DIR}/{clientname}-{servername}-{loadtype}.hey.txt 2> /dev/null &' 
        )
        host.cmd(cmd3)
