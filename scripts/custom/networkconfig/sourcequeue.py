# FIX THIS PART. MAP PER LAYER OF SWITCHES
# OUTPUT LIST OF SWITCHES PACKETS FROM A CERTAIN CLIENT WILL DEFINITELY PASS THROUGH (INITIAL)
# FIX CORE SWITCH
# PROBLEM: IF MULTIPLE CLIENTS HAVE SIMILAR SWITCHES
"""
This module emits the source.queue.map.q2 file which is used for source based queueing.
For each client, list the switches in the shortest path to the core, followed by a queue number.
Then, list the core switch, followed by the same queue number.
"""
import csv
import yaml
import range_divider
import math

def generate_conf(ip, leaf, queue, core):
	return f"10.0.0.{ip}\t{leaf}:{queue}\t{core}:{queue}\n"

def get_switches_path(l1_switch, fat_tree, layers):
	curr_switch = l1_switch
	switches = [curr_switch]
	for i in range(1, layers+1):
		index = fat_tree[i].index(f"switch{curr_switch}")
		# print (f"Curr Switch: {curr_switch}\tIndex: {index}\tIndex/2: {int(math.ceil(index/2))}")
		curr_switch = curr_switch + len(fat_tree[i]) - int(math.ceil(index/2))
		switches.append(curr_switch)
		# print (f"Layer 1 Switch: {l1_switch}\tSwitches: {switches}")
	return switches

def save_to_conf(basedir):

	config_file = open(f"{basedir}/source.queue.map.q2.tab", "w")
	yml = f"{basedir.split('custom')[0]}/simulate_topo.yml"
	with open (yml, 'rb') as yml_file:
		topo = yaml.load(yml_file, Loader=yaml.FullLoader)

	ceil = topo['topology']['fat_tree']['clients']
	layers = topo['topology']['fat_tree']['leaf_switch_layers']
	fat_tree = range_divider.switch_layers()
	divider = range_divider.divider(ceil, 2 ** layers)
	leaf_switches_cnt = 2 ** layers
	core_switch = [int(fat_tree[layers][1].split('h')[1])+1]
	rng_list = range_divider.divider(ceil, leaf_switches_cnt)
	rng_index = 0
	rng = rng_list[rng_index]
	l1_switch = 1
	queue = 0

	print (f"Fat Tree: {fat_tree}")
	print (f"\nDivider: {divider}")
	print (f"Core Switch: {core_switch}\n\n")

	for ip in  range (1, ceil+1):
		if queue > 2:
			queue = 0
		if ip <= rng_list[rng_index]:
			switches = get_switches_path(l1_switch, fat_tree, layers)
			config_file.write(generate_conf(ip, switches, queue, core_switch))
		else:
			rng_index = rng_index + 1
			l1_switch = rng_index + 1
			switches = get_switches_path(l1_switch, fat_tree, layers)
			config_file.write(generate_conf(ip, switches, queue, core_switch))
		queue = queue + 1

def main():
	save_to_conf()

if __name__ == '__main__':
	main()






















