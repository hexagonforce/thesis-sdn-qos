import os
from simulation.constants import SLEEP_CONST

BASEDIR = os.getcwd()

def test_convergence(net):
    client1 = net.getNodeByName('client1')
    server1 = net.getNodeByName('server1')
    client1.cmd(f'ping -c 50 {server1.IP()} > {BASEDIR}/simulation/test.results/pings/time_to_converge.txt')

def run_all_pings(net):
    clients = [host for host in net.hosts if 'client' in host.name]
    servers = [host for host in net.hosts if 'server' in host.name]

    for client in clients:
        for server in servers:
            client.cmd(f'ping -c 20 {server.IP()} > {BASEDIR}/simulation/test.results/pings/{client.name}-{server.name}.txt')
