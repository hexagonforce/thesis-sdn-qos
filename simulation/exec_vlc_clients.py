import os
import time
import shlex
from datetime import datetime

BASEDIR = os.getcwd()

def run(net, serverdata, loadconfig):
    pid_list = []
    for loadrow in loadconfig:
        clientname = loadrow[0]
        vlcload = loadrow[2].split('-')
        loadtype = vlcload[1]
        servernum = int(vlcload[2])

        host = net.getNodeByName(clientname)
        servername = f'server{servernum}'
        server = net.getNodeByName(servername)
        vlclogfilename = (
            f'{BASEDIR}/simulation/test.results/vlc-clients/run-vlc-client'
            f'-{loadtype}-{clientname}.{datetime.now().strftime("%m%d%Y%H%M%S")}'
        )
        results_filename = (
            f'{BASEDIR}/simulation/test.results/vlc-clients/results-{clientname}-{servername}'
            f'-{loadtype}.{datetime.now().strftime("%m%d%y_%H%M%S")}.csv'
        )
        media_url = f'rtsp://{server.IP()}:5004/{serverdata[servername][loadtype]}'
        duration = 300
        cmd = (
            f'sudo -u mininet python3 {BASEDIR}/simulation/run_vlc_client.py '
            f'{results_filename} {vlclogfilename} {media_url} {duration}'
        )
        vlc_process = host.popen(
            shlex.split(cmd),
            stderr=open(f'{BASEDIR}/simulation/test.results/vlc-clients/{clientname}error.txt', 'w')
        )
        pid_list.append(vlc_process)
        time.sleep(0.5)
    return pid_list
