import networkx as nx
import os

from scripts import network_topologies
from scripts.custom import network_configs, nodes_config

BASEDIR = os.getcwd()
def generate_graph(topology):
    return network_topologies.get_topology_graph(topology)

def configure(G, case):
    network_configs.generate_all_configs(G) # intention is to pass networkx graph to everyone
    nodes_config.write_all_config_to_json(case)
    nx.write_graphml(G, f'{BASEDIR}/config/topology.graphml')

if __name__ == '__main__':
    G = generate_graph()
    configure(G)
