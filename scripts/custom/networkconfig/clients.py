"""
This module takes the simulate_topo.yml (the topology description file)
and emits a client to switch map tab-delimited text file.
In other words, the contents of clientswtch.map.tab is a list of clients and the switches the clients are connected to.
"""

import os 
import yaml


def save_to_conf(basedir):
	path = f"{basedir}/clientswitch.map.tab"
	yml = f"{basedir}/topology_information.yml"
	with open (yml, 'rb') as yml_file:
		topo = yaml.load(yml_file, Loader=yaml.FullLoader)

	with open(path, 'w') as config_file:
		list_clients = topo['list_clients']

		for client in list_clients:
			switchnum = list(topo["adjlist"][client].keys())[0].replace("switch", "")
			config_file.write(f"{client}\t{switchnum}\n")

if __name__ == '__main__':
	save_to_conf(f"{os.getcwd()}/config/custom")




















