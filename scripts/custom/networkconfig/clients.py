"""
This module takes the simulate_topo.yml (the topology description file)
and emits a client to switch map tab-delimited text file.
In other words, the contents of clientswtch.map.tab is a list of clients and the switches the clients are connected to.
"""

import csv
import range_divider
import os 
import yaml


def generate_conf(i, switch):
	return f"client{i}\t{switch}\n"

def save_to_conf(basedir):
	path = f"{basedir}/clientswitch.map.tab"
	yml = f"{basedir.split('custom')[0]}simulate_topo.yml"
	if os.path.exists(path):
		os.remove(path)

	config_file = open(path, "w") # 
	with open (yml, 'rb') as yml_file:
		topo = yaml.load(yml_file, Loader=yaml.FullLoader)

	print (f"\n\n\n{topo}\n\n\n")
	ceil = topo['topology']['fat_tree']['details']['clients']
	print (f"CEIL: {ceil}")
	leaf_switches_cnt = 2 ** topo['topology']['fat_tree']['details']['leaf_switch_layers']
	rng_list = range_divider.divider(ceil, leaf_switches_cnt)
	print (f"range list: {rng_list}\n")
	rng_index = 0
	rng = rng_list[rng_index]
	switch = 1
	port = 1

	for i in  range (1, ceil+1):
		if i <= rng_list[rng_index]:
			config_file.write(generate_conf(i, switch))
		else:
			rng_index = rng_index + 1
			switch = rng_index + 1
			config_file.write(generate_conf(i, switch))

	config_file.close()






















