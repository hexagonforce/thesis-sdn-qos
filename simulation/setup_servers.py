from time import sleep
import telnetlib
import socket
import logging
import os.path, os
from datetime import datetime


BASEDIR = os.getcwd()
SIMULDIR = f"{BASEDIR}/simulation"

def run(net, serverdata):
    for servername, data in serverdata.items():
        server = net.getNodeByName(servername)
        if data['protocol'] == 'http':
            server.cmd(f'python3 -m http.server 80 --directory {SIMULDIR}/{servername} > /dev/null 2> /dev/null &')
        elif data['protocol'] == 'rtsp':
            vlcserversetup(server, data)

def vlcserversetup(server, data):
    logfilename = (
        f'{SIMULDIR}/test.results/vlc-server/results.run-vlc-server-'
        f'{server.IP()}.{datetime.now().strftime("%m%d%Y%H%M%S")}.log'
    )
    vlm_file = f"{SIMULDIR}/{data['vlm']}.vlm"
    cmd = (
        f'sudo -u mininet cvlc -vvv --file-logging --logfile={logfilename} '
        '--stats --color --rtsp-port 5004 --rtsp-throttle-users=0 '
        f'--network-caching=200000 --file-caching=200000 --vlm-conf={vlm_file} &'
    )
    server.cmd(cmd)
