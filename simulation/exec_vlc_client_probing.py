# $portToUse -c $clientname -s $9 -d $datetimestr -t $exectype -h $hostname
from datetime import datetime, timedelta
import os

BASEDIR = os.getcwd()
def run(net, serverdata, loadconfig):
    port_to_use = 4313
    for loadinfo in loadconfig:
        clientname = loadinfo[0]
        loadtypeinfo = loadinfo[2].split('-')
        exectype = loadtypeinfo[1]
        serverid = int(loadtypeinfo[2])
        starttime = datetime.now()
        datetimestr = str(starttime).replace(' ', '')
        endtime = starttime + timedelta(minutes=5)
        endtimestr = endtime.strftime("%m%d%Y%H%M%S")
        targetserver = f"10.0.1.{100+serverid}"
        hostnum = ''.join((c for c in clientname if c.isdigit()))
        hostname = f'10.0.0.{hostnum}'


        cmd = (
            f'python3 {BASEDIR}/simulation/vlcrctelnetclient.py -p {port_to_use} ' 
            f'-c {clientname} -s {targetserver} -d {datetimestr} -t '
            f'{exectype} -h {hostname} -e {endtimestr} &'
        )
        host = net.getNodeByName(clientname)
        host.pexec(cmd)
        port_to_use += 1