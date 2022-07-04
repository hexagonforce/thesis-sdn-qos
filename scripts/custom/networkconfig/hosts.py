# Generates hosts.conf which contains information about server and client hosts
# - name: the name of the host
# - switch: the switch that the host is connected to
# - port: the port of the switch that the host is connected to
# Server:
# 	- protocol: the protocol that the server responds to
#	- nwproto: the IP Protocol that the server uses (6 = TCP)
#	- tpdst: the destination port
# 	- proto_priority: the priority of the protocol (higher means more prioritized)
# 	- proto_queue_id: no idea
import csv
import yaml

NUMBER_OF_SERVERS = 6

def dpid(node):
	return int(''.join(c for c in node if c.isdigit()))

def generate_conf(i, switch, port):
	return f"10.0.0.{i}\tname=client{i}\tswitch={switch}\tport={port}\n"

def generate_server(i, switch, port, protocol, tpdst, priority, proto_queue_id, dst_queue_id):
	return f"10.0.1.{100 + i}\tname=server{i}\tswitch={switch}\tport={port}\tprotocol={protocol}\tnwproto=6\ttpdst={tpdst}\tproto_priority={priority}\tproto_queue_id={proto_queue_id}\tdst_queue_id={dst_queue_id}\n"

def save_to_conf(basedir):

	config_file = open(f"{basedir}/hosts.conf", "w")
	# print (f'config file: {config_file}')
	yml = f"{basedir}/topology_information.yml"
	with open (yml, 'rb') as yml_file:
		topo = yaml.load(yml_file, Loader=yaml.FullLoader)
	server_switch = topo['server_switch']
	
	for client in topo['list_clients']:
		i = dpid(client)
		for switch in topo['adjlist'][client]:
			port = topo['adjlist'][switch][client]
			config_file.write(generate_conf(i, dpid(switch), port))

	for server in topo['list_servers']:
		i = dpid(server)
		for switch in topo['adjlist'][server]:
			port = topo['adjlist'][switch][server]
			if i % 2 == 0:
				config_file.write(generate_server(i, dpid(server_switch), port, 'vlc', 5004, 1000, 1, i-1))
			else:
				config_file.write(generate_server(i, dpid(server_switch), port, 'http', 80, 100, 0, i-1))

def main():
	save_to_conf()

if __name__ == '__main__':
	main()






















