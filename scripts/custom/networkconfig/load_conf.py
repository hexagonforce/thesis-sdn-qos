# 
# This module takes the topology file and emits the corresponding
# load configuration file in config/custom/load.conf.l3.tab
# Each client is assigned to a combination of the following types of requests:
# - http and vlc
# - low and high bandwith
# - options 1, 2 and 3 which are http1 http2 http3 servers and vlc1 vlc2 and vlc3 servers.
# 

from pathlib import Path
from util.conf_util import get_yml_data
from util.constants import SERVERCONF

def get_number_of_servers():
	serverdata = get_yml_data(SERVERCONF)
	http = sum(map(lambda data: data['protocol'] == 'http', serverdata.values()))
	rtsp = sum(map(lambda data: data['protocol'] == 'rtsp', serverdata.values()))
	return http, rtsp

def generate_conf(client, http, vlc, val, val2):
	return f"{client}\thttp-{http}-{val}\tvod-{vlc}-{val2}\n"

def nth_odd(n): # 0th odd number is 1
	return 2 * n + 1
def nth_even(n): # 0th even number is 2
	return 2 * n + 2

def save_to_conf(basedir, G):
	HTTP_SERVERS, VLC_SERVERS = get_number_of_servers()
	types = ['medium', 'high']
	list_clients = [node for node, data in G.nodes(data='type') if data=='client']
	list_clients.sort(key= lambda x: int(x.replace('client', '')))
	#list_clients.reverse() # this is an experiment
	with open(f"{basedir}/load.conf.l3.tab", "w") as config_file:
		for idx, client in enumerate(list_clients):
			typeidx = idx % (HTTP_SERVERS + VLC_SERVERS) // len(types)
			httpservernum = nth_odd(idx % HTTP_SERVERS)
			vlcservernum = nth_even(idx % VLC_SERVERS)
			config_file.write(generate_conf(client, types[typeidx], types[typeidx], httpservernum, vlcservernum))
