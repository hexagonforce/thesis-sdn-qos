import os.path, os
from datetime import datetime
import shlex
import subprocess

BASEDIR = os.getcwd()
SIMULDIR = f"{BASEDIR}/simulation"

def run(net, serverdata):
    pid_list = []
    for servername, data in serverdata.items():
        server = net.getNodeByName(servername)
        if data['protocol'] == 'http':
            p = server.popen(
                shlex.split(f'python3 -m http.server 80 --directory {SIMULDIR}/{servername}'),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            pid_list.append(p)
        elif data['protocol'] == 'rtsp':
            pid_list.append(vlcserversetup(server, data))
    return pid_list

def vlcserversetup(server, data):
    logfilename = (
        f'{SIMULDIR}/server-logs/results.run-vlc-server-'
        f'{server.IP()}.{datetime.now().strftime("%m%d%Y%H%M%S")}.log'
    )
    vlm_file = f"{SIMULDIR}/{data['vlm']}.vlm"
    cmd = (
        f'sudo -u mininet cvlc -vvv --file-logging --logfile={logfilename} '
        '--stats --color --rtsp-port 5004 --rtsp-throttle-users=0 --rtsp-timeout=300 --rtsp-session-timeout=300'
        f'--network-caching=200000 --file-caching=200000 --vlm-conf={vlm_file} &'
    )
    p = server.popen(
        shlex.split(cmd)
    )
    return p
