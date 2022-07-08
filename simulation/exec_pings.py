import os, subprocess
from simulation.constants import SLEEP_CONST

BASEDIR = os.getcwd()
def run(net):
    subprocess.run(['sh', '-c', f'rm {BASEDIR}/simulation/test.results/pings/*.txt'])
    clients = [host for host in net.hosts if 'client' in host.name]
    servers = [host for host in net.hosts if 'server' in host.name]
    client1 = net.getNodeByName('client1')
    server1 = net.getNodeByName('server1')
    client1.cmd(f'ping -c 50 {server1.IP()} > {BASEDIR}/simulation/test.results/pings/time_to_converge.txt')
    for server in servers[::2]:
        for client in clients:
            client.cmd(f'ping -c 20 {server.IP()} >> {BASEDIR}/simulation/test.results/pings/{client.name}.txt')