import csv
import subprocess
import os
from pathlib import Path
import yaml

BASEDIR = os.getcwd()
ABTESTS_DIR = f'{BASEDIR}/simulation/test.results/ab-tests'
def run(net, serverdata, loadconfig):
    subprocess.call(['sh', '-c', f'rm {ABTESTS_DIR}/*'])
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
            'sudo -u mininet ab -l -r -n 50000 -c 10 -k -t 240 -s 240 '
            f'-q -H "Accept-Encoding: gzip, deflate" http://{server.IP()}/{file} > '
            f'{ABTESTS_DIR}/{clientname}-{servername}-{loadtype} &'
        )
        cmd2 = (
            'sudo -u mininet wrk --header "Accept-Encoding: gzip, deflate" -c 10 '
            f'-d 240 --timeout 240 http://{server.IP()}/{file} > '
            f'{ABTESTS_DIR}/{clientname}-{servername}-{loadtype} 2> /dev/null &'
        )
        host.cmd(cmd)