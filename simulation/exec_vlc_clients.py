import os
import time
from datetime import datetime
BASEDIR = os.getcwd()

def run(net, serverdata, loadconfig):

    portnum = 4313
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
            f'-{loadtype}-{portnum}-{host.IP()}.{datetime.now().strftime("%m%d%Y%H%M%S")}'
        )
        cmd = (
            f'sudo -u mininet cvlc -vvv --file-logging -logfile={vlclogfilename} '
            f'--intf rc --rc-host={host.IP()}:{portnum} -Vdummy --noaudio --novideo '
            '--rc-fake-tty --no-sout-display-video --no-sout-display-audio '
            '--no-playlist-autostart --no-video-deco --no-embedded-video --input-repeat=5 '
            f'--quiet rtsp://{server.IP()}:5004/{serverdata[servername][loadtype]} &'
        )
        host.pexec(cmd)
        portnum += 1