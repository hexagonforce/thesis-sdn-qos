from time import sleep
import telnetlib
import socket
import logging
import os.path, os
from datetime import datetime


BASEDIR = os.getcwd()
SIMULDIR = f"{BASEDIR}/simulation"

def setup_servers(net, serverdata):
    for servername, data in serverdata.items():
        server = net.getNodeByName(servername)
        if data['protocol'] == 'http':
            server.cmd(f'python3 -m http.server 80 --directory {SIMULDIR}/{servername} &')
        elif data['protocol'] == 'rtsp':
            pass # vlcserversetup(server, data)

def vlcserversetup(server, data):
    logfilename = (
        f'{SIMULDIR}/test.results/vlc-server/results.run-vlc-server-'
        f'{server.IP()}.{datetime.now().strftime("%m%d%Y%H%M%S")}.log'
    )
    cmd = (
        f'sudo -u mininet cvlc -vvv --file-logging --logfile={logfilename}'
        ' --stats --color I telnet --telnet-password mininet --rtsp-port 5004'
        ' --rtsp-throttle-users 0 --network-caching=2000 --file=caching=200000 &'
    )
    server.cmd(cmd)
    sleep(5)
    telnetStartVLCServer(server.IP(), data['vlm'])

def telnetStartVLCServer(servername, argv):
    logging.basicConfig(level=logging.DEBUG,
                        filename='telnetStartVLC.log', 
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    logging.info("\n\n")
    timeout = 120
    logging.info("Attempting to start telnet vlc")
    port = 4212
    clientname = servername
    logging.info("ARGV: {}".format(argv))
    vlm_file = f'{argv}.vlm'
    vlm_load = f"load {SIMULDIR}/{vlm_file}"

    logging.info ("Connecting...")
    try:
        session = telnetlib.Telnet(clientname, port, timeout)
    except socket.timeout:
        logging.info ("socket timeout")
    else:
        output = session.read_until(b"Password:", timeout)
        logging.info("First output: {}".format(output))
        session.write("mininet".encode('ascii') + b"\r\n")
        output = session.read_until(b">", timeout )
        logging.info("Second output: {}".format(output))
        session.write(vlm_load.encode('ascii') + b"\r\n")
        eager = session.read_very_eager()
        output = session.read_until(b">", timeout )
        logging.info("Loading BBBVLCConfig output: {}".format(output))
        logging.info("Detailed Output: {}".format(eager))
        session.write("show media".encode('ascii') + b"\r\n")
        media = session.read_very_eager()
        logging.info("Media: {}".format(media))
        session.write("quit".encode('ascii') + b"\r\n")
        
        session.close()
        logging.info("Closing Session")