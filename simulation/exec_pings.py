import os, subprocess, time
from simulation.constants import SLEEP_CONST
from mininet.util import pmonitor

BASEDIR = os.getcwd()

def test_convergence(net):
    client1 = net.getNodeByName('client1')
    server1 = net.getNodeByName('server1')
    client1.cmd(f'ping -c 50 {server1.IP()} > {BASEDIR}/simulation/test.results/pings/time_to_converge.txt')

def run_all_pings(net):
    clients = [host for host in net.hosts if 'client' in host.name]
    servers = [host for host in net.hosts if 'server' in host.name]

    for client in clients:
        popens = {}
        outfiles = []
        for server in servers:
            outfiles.append(open(f'{BASEDIR}/simulation/test.results/pings/{client.name}-{server.name}.txt', 'w'))
            popens[server] = client.popen(f'ping -c 20 {server.IP()}', stdout=outfiles[-1])
        while sum((1 for p in popens.values() if p.poll() is None)) != 0:
            time.sleep(SLEEP_CONST)
        for outfile in outfiles:
            outfile.close()
