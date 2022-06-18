# Generates hosts.conf which contains information about server and client hosts
# - name: the name of the host
# - switch: the switch that the host is connected to
# - port: the port of the switch that the host is connected to
# Server:
# 	- protocol: the protocol that the server responds to
#	- nwproto: the IP Protocol that the server uses (6 = TCP)
#	- tpdst: the destination port
# 	- proto_priority: the priority of the protocol (higher means more prioritized)
# 	- proto_queue_id: 
import csv
import yaml
import range_divider


def generate_conf(i, switch, port):
	return f"10.0.0.{i}\tname=client{i}\tswitch={switch}\tport={port}\t\n"

def generate_server(i, switch, port, protocol, tpdst, priority, proto_queue_id, dst_queue_id):
	return f"10.0.1.10{i}\tname=server{i}\tswitch={switch}\tport={port}\tprotocol={protocol}\tnwproto=6\ttpdst={tpdst}\tproto_priority={priority}\tproto_queue_id={proto_queue_id}\tdst_queue_id={dst_queue_id}\n"

def save_to_conf(basedir):

	config_file = open(f"{basedir}/hosts.conf", "w")
	print (f'config file: {config_file}')
	yml = f"{basedir.split('custom')[0]}/simulate_topo.yml"
	with open (yml, 'rb') as yml_file:
		topo = yaml.load(yml_file, Loader=yaml.FullLoader)

	ceil = topo['topology']['fat_tree']['clients']
	layers = topo['topology']['fat_tree']['leaf_switch_layers']
	leaf_switches_cnt = 2 ** layers
	total_switches = 2 ** (layers + 1)
	rng_list = range_divider.divider(ceil, leaf_switches_cnt)
	rng_index = 0
	rng = rng_list[rng_index]
	switch = 1
	port = 1
	powers_2 = []
	for i in range(1, layers+1):
		powers_2.append(2**i)

	powers_2.reverse()
	print (powers_2)

	# if layers > 1:
	# 			switches = [switch]
	# 			sw = switch
	# 			for j in powers_2:
	# 				sw = sw + j
	# 				switches.append(sw)
	# 			print (f"Client: {i}\tSwitches: {switches}")
	# 		else:

	for i in  range (1, ceil+1):
		if i <= rng_list[rng_index]:
			config_file.write(generate_conf(i, switch, port))
		else:
			rng_index = rng_index + 1
			switch = rng_index + 1
			port = 1
			config_file.write(generate_conf(i, switch, port))
		port = port + 1

	for i in range(1, 7):
		port = i + 1
		if i % 2 == 0:
			config_file.write(generate_server(i, total_switches, port, 'vlc', 5004, 1000, 1, i-1))
		else:
			config_file.write(generate_server(i, total_switches, port, 'http', 80, 100, 0, i-1))

def main():
	save_to_conf()

if __name__ == '__main__':
	main()






















