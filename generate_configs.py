'''
Legacy script for stand-alone config generation without running the entire simulation
'''
import networkx as nx
import os

from scripts import network_topologies
from scripts.custom import network_configs, nodes_config
from util.constants import RUNCONF, BASEDIR
from util.conf_util import get_yml_data

def configure(G, case):
    network_configs.generate_all_configs(G) # intention is to pass networkx graph to everyone
    nodes_config.write_all_config_to_json(case)
    nx.write_graphml(G, f'{BASEDIR}/config/topology.graphml')

if __name__ == '__main__':
    runconf = get_yml_data(RUNCONF)
    topology = runconf['topology']
    casenum = runconf['case']
    G = network_topologies.get_topology_graph(topology)
    configure(G)
