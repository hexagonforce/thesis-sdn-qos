"""
This module takes the simulate_topo.yml (the topology description file)
and emits a client to switch map tab-delimited text file.
In other words, the contents of clientswtch.map.tab is a list of clients and the switches the clients are connected to.
"""

import os 
import yaml

def save_to_conf(basedir, G):
    list_clients = [node for node, data in G.nodes(data='type') if data=='client']
    with open(f'{basedir}/clientswitch.map.tab', 'w') as config_file:
        for client in list_clients:
            switch_num = list(G[client].keys())[0].replace('switch', '')
            config_file.write(f'{client}\t{switch_num}\n')
