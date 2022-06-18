"""
This module emits a usecase_nodes_configuration pickle file
and a usecase_nodes_configuration json file for use by I have absolutely no idea.
It reads from the files emitted by network_configs.py.
"""


import pickle
import os
import csv
import yaml
import json

from json import JSONEncoder


from networkconfig.get_node_entries import get_host_entries
from networkconfig.get_node_entries import get_switch_entries
from networkconfig.node_classes import Host
from networkconfig.node_classes import Switch

BASEDIR = os.getcwd()
# print BASEDIR
# print "\n\n"
PARDIR = "{}/config/custom".format(BASEDIR)
OUTDIR = "{}/pkl/net_data".format(BASEDIR)

yml = "{}/gen_config.yml".format(PARDIR)

config_data = {
	'usecase' : '',
	'sourceQueueMapDict' : {},
	'traffic' : {},
	'host_entries' : {},
	'switches_entries' : {},
	'hosts_list' : [],
	'clients_list' : [],
	'servers_list' : [],
	'switches_list' : {},
}

exec_data = {
	'load_config' : {},
	'client_switch_map' : {},
}

class DataEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

with open(yml,'rb') as yml_file:
	yml_data = yaml.load(yml_file) # , Loader=yaml.FullLoader

config_path = {
	'hostsfile' : "{}/{}".format(PARDIR, yml_data['nodes_config']['hostsfile']),
	'switchesfile' : "{}/{}{}.conf".format(PARDIR, yml_data['nodes_config']['switchesfile'], yml_data['case']),
	'sourcequeuemapfile' : "{}/{}".format(PARDIR, yml_data['nodes_config']['sourcequeuemapfile']),
	'traffic_class' : "{}/{}".format(PARDIR, yml_data['nodes_config']['traffic_class']),
	'clientconfig_file' : "{}/{}".format(PARDIR, yml_data['exec_config']['clientconfig']),
	'clientswitch_file' : "{}/{}".format(PARDIR, yml_data['exec_config']['clientswitch'])
}

config_data['usecase'] = yml_data['case']
# pkl = "{}/usecase_{}_nodes_configuration.pkl".format(OUTDIR, config_data['usecase'])
exec_pkl = "{}/usecase_{}_exec.pkl".format(OUTDIR, config_data['usecase'])

js = "{}/usecase_{}_nodes_configuration.json".format(PARDIR, config_data['usecase'])
# exec_pkl = "{}/usecase_{}_exec.json".format(PARDIR, config_data['usecase'])

# Get Source-Queue Map File
with open(config_path['sourcequeuemapfile'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		config_data['sourceQueueMapDict'][row[0]] = row[1:]

print ("\n\n\nsourceQueueMapDict: {}\n\n\n".format(config_data['sourceQueueMapDict']))

# Get traffic class
with open(config_path['traffic_class'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		protocol = row[0].split('=')[1]
		config_data['traffic'][protocol] = {}
		for item in row[1:]:
			item = item.split('=')
			values = item[1].split(',')
			if len(values) > 1:
				values = [int(v) for v in values]
				config_data['traffic'][protocol][item[0]] = values
			else:
				config_data['traffic'][protocol][item[0]] = int(item[1])

# Get Hosts File
with open(config_path['hostsfile'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		config_data['host_entries'][row[0]] = row[1:]

with open(config_path['switchesfile'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		config_data['switches_entries'][row[0]] = row # row[1:]

print ("\n\n\n\n")
print (config_path['switchesfile'])
print ("\n\n\n\n")

config_data['hosts_list'] = get_host_entries(config_data['host_entries'])[0]
config_data['clients_list'] = get_host_entries(config_data['host_entries'])[1]
config_data['servers_list']  = get_host_entries(config_data['host_entries'])[2]
config_data['switches_list'] = get_switch_entries(config_data['switches_entries'], 
													config_data['hosts_list'], 
													config_data['clients_list'], 
													config_data['servers_list']
												)

# print ("Clients List: {}".format(config_data['clients_list'][0].layered_switches))

with open(config_path['clientconfig_file'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		exec_data['load_config'][row[0]] = row[1:]

with open(config_path['clientswitch_file'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		exec_data['client_switch_map'][row[0]] = row[1:]

if os.path.exists(js):
	os.remove(js)

print (f"config: {config_data.keys()}\n\n")
# print (f'exec: {exec_data}\n\n')

for host in config_data['servers_list']:
	print (f"{type(host)}\t\t{host}")

# config_json = json.dumps(config_data, indent=4, cls=DataEncoder)
# exec_json = json.dumps(exec_data, indent=4)

# print (config_json)

print ('\n\n')

# print (exec_json)

with open(js, 'w') as json_file:
	print (f"\n\nJSON File: {json_file}\n\n")
	config_json = json.dumps(config_data, indent=4, cls=DataEncoder)
	json_file.write(config_json)
	# json.dump(config_data, json_file)
	# pickle.dump(config_data, pkl_file, pickle.HIGHEST_PROTOCOL)
	# pickle.dump(config_data, pkl_file, 2) # , pickle.DEFAULT_PROTOCOL

with open(exec_pkl, 'wb') as pkl_file:
	# pickle.dump(config_data, pkl_file, pickle.HIGHEST_PROTOCOL)
	pickle.dump(exec_data, pkl_file, 2) # , pickle.DEFAULT_PROTOCOL







