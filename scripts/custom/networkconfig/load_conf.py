# 
# This module takes the topology file and emits the corresponding
# load configuration file in config/custom/load.conf.l3.tab
# Each client is assigned to a combination of the following types of requests:
# - http and vlc
# - low and high bandwith
# - options 1, 2 and 3 which are http1 http2 http3 servers and vlc1 vlc2 and vlc3 servers.
# 

import csv
import yaml, os


def generate_conf(client, http, vlc, val, val2):
	return f"{client}\thttp-{http}-{val}\tvod-{vlc}-{val2}\n"

HTTP_SERVERS = 2
VLC_SERVERS = 2

def save_to_conf(basedir):
	config_file = open(f"{basedir}/load.conf.l3.tab", "w")
	types = ['medium', 'high']
	yml = f"{basedir}/topology_information.yml"
	with open (yml, 'rb') as yml_file:
		topo = yaml.load(yml_file, Loader=yaml.FullLoader)

	def nth_odd(n): # 0th odd number is 1
		return 2 * n + 1
	def nth_even(n): # 0th even number is 2
		return 2 * n + 2
	
	for idx, client in enumerate(topo['list_clients']):
		typeidx = idx // (HTTP_SERVERS + VLC_SERVERS) % len(types)
		httpservernum = nth_odd(idx % HTTP_SERVERS)
		vlcservernum = nth_even(idx % VLC_SERVERS)
		config_file.write(generate_conf(client, types[typeidx], types[typeidx], httpservernum, vlcservernum))

def main():
	save_to_conf(f'{os.getcwd()}/config/custom')

if __name__ == '__main__':
	main()
