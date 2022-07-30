"""
Inputs: The gen_config.yml file, and all the files generated by scripts/custom/network_configs.py
Outputs: The nodes configuration in config/usecase_{usecase}_nodes_configuration.json
"""


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
PARDIR = f"{BASEDIR}/config/custom"
yml = f"{BASEDIR}/config/gen_config.yml"

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
	yml_data = yaml.load(yml_file, Loader=yaml.FullLoader) # 

config_path = {
	'hostsfile' : "{}/{}".format(PARDIR, yml_data['nodes_config']['hostsfile']),
	'switchesfile' : "{}/{}{}.conf".format(PARDIR, yml_data['nodes_config']['switchesfile'], yml_data['case']),
	'sourcequeuemapfile' : "{}/{}".format(PARDIR, yml_data['nodes_config']['sourcequeuemapfile']),
	'traffic_class' : f"{BASEDIR}/config/traffic_class.yml",
	'clientconfig_file' : "{}/{}".format(PARDIR, yml_data['exec_config']['clientconfig']),
	'clientswitch_file' : "{}/{}".format(PARDIR, yml_data['exec_config']['clientswitch'])
}

config_data['usecase'] = yml_data['case']
js = "{}/usecase_{}_nodes_configuration.json".format(PARDIR, config_data['usecase'])

# # Get Source-Queue Map File
# with open(config_path['sourcequeuemapfile'], 'rt') as csv_file:
# 	for row in csv.reader(csv_file, delimiter='\t'):
# 		config_data['sourceQueueMapDict'][row[0]] = row[1:]

# Get traffic class
with open(config_path['traffic_class'], 'rt') as traffic_yml:
	traffic = yaml.load(traffic_yml, Loader=yaml.FullLoader)
	for protocol, details in traffic.items():
		config_data['traffic'][protocol] = details

# Get Hosts File
with open(config_path['hostsfile'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		config_data['host_entries'][row[0]] = row[1:]

with open(config_path['switchesfile'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		config_data['switches_entries'][row[0]] = row # row[1:]

config_data['hosts_list'] = get_host_entries(config_data['host_entries'])[0]
config_data['clients_list'] = get_host_entries(config_data['host_entries'])[1]
config_data['servers_list']  = get_host_entries(config_data['host_entries'])[2]
config_data['switches_list'] = get_switch_entries(config_data['switches_entries'], 
													config_data['hosts_list'], 
													config_data['clients_list'], 
													config_data['servers_list']
												)

with open(config_path['clientconfig_file'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		exec_data['load_config'][row[0]] = row[1:]

with open(config_path['clientswitch_file'], 'rt') as csv_file:
	for row in csv.reader(csv_file, delimiter='\t'):
		exec_data['client_switch_map'][row[0]] = row[1:]

if os.path.exists(js):
	os.remove(js)


with open(js, 'w') as json_file:
	config_json = json.dumps(config_data, indent=4, cls=DataEncoder)
	json_file.write(config_json)







