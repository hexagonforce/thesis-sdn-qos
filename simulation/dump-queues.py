import yaml
import os

configdir = f'{os.getcwd()}/config/custom/topology_information.yml'

with open(configdir, 'r') as topoinfo:
    topo = yaml.load(topoinfo, Loader=yaml.FullLoader)

all_switches = []
all_switches.append(topo['core_switch'])
all_switches += topo['internal_switches']
all_switches += topo['edge_switches']
all_switches.append(topo['server_switch'])

for switch in all_switches:
    os.system(f'sudo ovs-ofctl -O Openflow13 queue-stats {switch} > {os.getcwd()}/simulation/test.results/queuestats/{switch}.txt')