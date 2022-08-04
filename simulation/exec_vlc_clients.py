import os
import time
from datetime import datetime
import vlc
BASEDIR = os.getcwd()

def run(net, serverdata, loadconfig, starttime):
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
        starttimestring = starttime.isoformat(timespec='seconds')
        duration = 300
        cmd = (
            f'sudo -u mininet python3 {BASEDIR}/simulation/run_vlc_client.py '
            f'{results_filename} {vlclogfilename} {media_url} {starttimestring} {duration} 2> {BASEDIR}/simulation/test.results/vlc-clients/{clientname}error.txt &'
        )
        host.cmd(cmd)
        time.sleep(1)
