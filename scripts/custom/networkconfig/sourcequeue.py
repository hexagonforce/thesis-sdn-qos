"""
This module emits the source.queue.map.q2 file which is used for source based queueing.
For each client, list the switches in the shortest path to the core, followed by a queue number.
Then, list the core switch, followed by the same queue number.
"""
import math

def generate_conf(ip, queue):
	return f"10.0.0.{ip}\t{queue}\n"

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

def save_to_conf(basedir, G):
	num_clients = sum(1 for node in G.nodes(data='type') if node[1] == 'client')
	queue = 0
	with open(f"{basedir}/source.queue.map.q2.tab", "w") as config_file:
		for ip in  range (1, num_clients+1):
			if queue > 2:
				queue = 0
			config_file.write(generate_conf(ip, queue))
			queue = queue + 1
