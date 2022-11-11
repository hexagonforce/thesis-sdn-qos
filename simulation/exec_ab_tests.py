import shlex
import os
import subprocess

BASEDIR = os.getcwd()
ABTESTS_DIR = f'{BASEDIR}/simulation/test.results/ab-tests'
def run(net, serverdata, loadconfig):
    pid_list = []
    for loadrow in loadconfig:
        clientname = loadrow[0]
        httpload = loadrow[1].split('-')
        loadtype = httpload[1]

        servernum = int(httpload[2])
        servername = f'server{servernum}'
        currserverdata = serverdata[servername]

        filename = currserverdata[loadtype]
        host = net.getNodeByName(clientname)
        server = net.getNodeByName(servername)

        cmd = (
            'hey -A "Accept-Encoding: gzip, deflate" -c 10 '
            f'-z 300s -t 300 \'http://{server.IP()}/{filename}\''
        )

        hey_process = host.popen(
            shlex.split(cmd), 
            stdout=open(f'{ABTESTS_DIR}/{clientname}-{servername}-{loadtype}.hey.txt', 'w'), 
            stderr=subprocess.DEVNULL
        )
        pid_list.append(hey_process)
    return pid_list
