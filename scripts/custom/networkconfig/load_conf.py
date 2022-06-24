# 
# This module takes the topology file and emits the corresponding
# load configuration file in config/custom/load.conf.l3.tab
# Each client is assigned to a combination of the following types of requests:
# - http and vlc
# - low and high bandwith
# - options 1, 2 and 3 which are http1 http2 http3 servers and vlc1 vlc2 and vlc3 servers.
# 

import csv
import yaml


def generate_conf(client, http, vlc, val):
	return f"{client}\thttp-{http}-{val}\tvod-{vlc}-{val}\n"

def save_to_conf(basedir):

	config_file = open(f"{basedir}/load.conf.l3.tab", "w")
	types = ['low', 'high']
	val = 1
	http = 0
	vlc = 0
	h_counter = 0
	v_counter = 0
	yml = f"{basedir}/topology_information.yml"
	with open (yml, 'rb') as yml_file:
		topo = yaml.load(yml_file, Loader=yaml.FullLoader)

	for client in topo['list_clients']: # this is so badly written that I'm not bothering to fix this
		h_counter = h_counter + 1
		v_counter = v_counter + 1
		if val > 3:
			val = 1
		config_file.write(generate_conf(client, types[http], types[vlc], val))
		val = val + 1

		if h_counter == 6:
			h_counter = 0
			if http == 0:
				http = 1
			else:
				http = 0

		if v_counter == 6:
			v_counter = 0
			if vlc == 0:
				vlc = 1
			else:
				vlc = 0

def main():
	save_to_conf()

if __name__ == '__main__':
	main()






















