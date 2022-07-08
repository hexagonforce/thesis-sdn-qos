# This module changes the measure/run-ipstat.sh file.
# It literally only changes the switch number depending on what the name of the root switch is.
#

import re
import os
import yaml

BASEDIR = os.getcwd()
ifstat = f"{BASEDIR}/simulation/run-ipstat.sh"
TOPO_INFO = f'{BASEDIR}/config/custom/topology_information.yml'

filein = open(ifstat, 'rt')
cmd = filein.read()

with open(TOPO_INFO, 'r') as yml_data:
    topo_data = yaml.load(yml_data, Loader=yaml.FullLoader)

core_switch = topo_data['core_switch']
server_switch = topo_data['server_switch']

core_switch_port = 0
for dest, port in topo_data['adjlist'][core_switch].items():
    if (dest == server_switch):
        core_switch_port = port
        break

core_switch = f'{core_switch}-eth{core_switch_port}'

init_intf = re.search("switch.*-eth.*", cmd)
changed_intf = init_intf.group().split(" ")[0]
cmd = cmd.replace(changed_intf, core_switch)
fileout = open(ifstat, 'wt')
fileout.write(cmd)
fileout.close()
os.system(f"chmod a+x {ifstat}")





