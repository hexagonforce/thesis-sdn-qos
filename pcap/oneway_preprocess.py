import os
import time
import yaml
import math
import json

import pandas as pd

BASEDIR = os.getcwd().split('pcap')[0]

topo_yml = f"{BASEDIR}config/simulate_topo.yml"

os.system('tshark -T fields -n -r smallFlows.pcap -E header=y -E separator=, -E occurrence=f -e ip.src -e ip.dst > ip.csv')

ip_list = []

df = pd.read_csv('ip.csv')

ip_list = df['ip.src'].dropna().tolist() + df['ip.dst'].dropna().tolist()
ip_list = list(set(ip_list))

with open(topo_yml, 'rb') as yml_file:
	topo = yaml.load(yml_file, Loader=yaml.FullLoader)['topology']
	hosts = topo[list(topo.keys())[0]]['details']['clients']

chunks = math.ceil(len(ip_list) / 5)
vhosts = {}

def get_chunks(lst, hosts, chunks):
	for i in range(0, len(lst), chunks):
		yield lst[i:i+chunks]

gen = get_chunks(ip_list, hosts, chunks)

for i in range(1,hosts+1):
	vhosts[f"vhost{i}"] = next(gen)

# print (vhosts)

total = []

for vhost in vhosts:
	total += vhosts[vhost]

vhosts_json = json.dumps(vhosts, indent=4)

with open('vhost_mapping.json', 'w') as json_file:
	json_file.write(vhosts_json)

























