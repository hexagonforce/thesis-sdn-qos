"""
    Functions in this module should output a yml file containing the client hosts, server hosts, switches,
    and all the links in the following order:

    First, we connect all the edge swtiches to the clients.
    Then, we connect all the edges within the switches.
    Then, we connect a "core" switch (defined to be the switch1) to the server switch
    Finally, we connect all the server hosts to the server switch.

    To have more switches in the server side, please modify the code yourself, as that
    is not within the scope of this research framework.

    Switches have the following types: server, core, edge, internal.

    The functions should return the following:
    result = {
        "core_switch" : core_switch,
        "internal_switches": internal_switches,
        "edge_switches": edge_switches,
        "server_switch": server_switch,
        "list_clients": list_clients,
        "list_servers": list_servers,
        "adjlist": adjlist,
        "edgelist": edgelist
    }
"""

import yaml
import os
import networkx as nx

BASEDIR = os.getcwd()
NUM_SERVERS = 4
INFTY = 10000000000000

def divider(clients, leaves):
    """
    Evenly divides the clients to the leaf switches and gives the 
    last client numbers per leaf (1 indexed)
    example: 70 Clients and 8 Leaves will result in 2 leaves with 8 clients and 6 leaves with 9 clients, therefore the output of 
    divider(70, 8) is [0, 8, 16, 25, 34, 43, 52, 61, 70]
    """
    clients_per_leaf = clients // leaves
    remaining_clients = clients % leaves
    last_client_number_list = [0, clients_per_leaf]
    for i in range(1, leaves):
        if i == leaves - remaining_clients:
            clients_per_leaf += 1
        last_client_number_list.append(clients_per_leaf + last_client_number_list[-1])
        
    return last_client_number_list

def farthest_by_hops(G):
    '''
    This function gives the id of the node of a NetworkX graph
    that has the highest sum of its distances to all other nodes
    '''
    dist_table = nx.floyd_warshall(G)
    res = 0
    maxdist = -INFTY
    for id, row in dist_table.items():
        sumdist = sum(list(row.values()))
        if sumdist > maxdist:
            res = id
            maxdist = sumdist
    return res

def generate_topology2(G, topo):
    num_switches = nx.number_of_nodes(G)
    
    # Assign core switch if it has not been assigned previously
    if 'core_switch_num' in topo['details']:
        core_switch_num = int(topo['details']['core_switch_num'])
    else:
        core_switch_num = int(farthest_by_hops(G)) + 1

    core_switch = f'switch{core_switch_num}'
    server_switch = f'switch{num_switches + 1}'

    # Get all the necessary details
    num_client_switches = topo['details']['client_switches']
    if num_client_switches == 'max' or num_client_switches > num_switches - 1:
        num_client_switches = num_switches - 1
    num_clients = topo['details']['clients']

    G = nx.relabel_nodes(G, lambda x : f'switch{int(x)+1}')
    G.add_node(server_switch)

    for x in G:
        G.nodes[x]['type'] = 'switch'

    for i in range(1, num_clients + 1):
        G.add_node(f'client{i}', type='client')

    for i in range(1, NUM_SERVERS + 1):
        G.add_node(f'server{i}', type='server')

    G.graph['core_switch'] = core_switch
    G.graph['server_switch'] = server_switch

    G.add_edge(G.graph['server_switch'], G.graph['core_switch'])

    normal_switches = [node for node, type in G.nodes(data='type') if type == 'switch']
    normal_switches.remove(core_switch)
    normal_switches.remove(server_switch)
    normal_switches = sorted(normal_switches, key=lambda x: int(x.replace('switch', '')))
    
    edge_switches = normal_switches[-num_client_switches:] # last few elements
    internal_switches = normal_switches[:-num_client_switches] # elements that are not edge switches

    for edge_switch in edge_switches:
        G.nodes[edge_switch]['type'] = 'edge_switch'
    for internal_switch in internal_switches:
        G.nodes[internal_switch]['type'] = 'internal_switch'

    client_ranges = divider(num_clients, num_client_switches)
    for idx, (prev, upper_bound) in enumerate(zip(client_ranges, client_ranges[1:])):
        for clientnum in range(prev + 1, upper_bound + 1):
            G.add_edge(edge_switches[idx], f'client{clientnum}')

    # add the servers to the server switch
    for server in [node for node, type in G.nodes(data='type') if type == 'server']:
        G.add_edge(server, G.graph['server_switch'])

    for node in sorted(G.nodes):
        for idx, edge in enumerate(sorted(G.edges(node))):
            port_number = idx
            if node.startswith('switch'):
                port_number += 1
            if not 'lport' in G.edges[edge]:
                G.edges[edge]['lport'] = port_number
            else:
                G.edges[edge]['rport'] = port_number

    return G

# Actual Topologies
def fat_tree(topo):
    layers = topo['details']['leaf_switch_layers']
    fanout = topo['details']['fanout']
    topo['details']['client_switches'] = fanout ** layers
    topo['details']['core_switch_num'] = 1

    G = nx.balanced_tree(fanout, layers)
    G.graph['name'] = f'fat_tree_{fanout}_{layers}'
    return generate_topology2(G, topo)

def mesh(topo):
    num_switches = topo['details']['switches']
    G = nx.complete_graph(num_switches)
    G.graph['name'] = f'mesh_{num_switches}'
    return generate_topology2(G, topo)

def zoo_data(topo):
    filename = topo['details']['filename']
    filepath = f'{BASEDIR}/zoo_data/{filename}'
    G = nx.read_graphml(filepath)
    G.graph['name'] = filename.replace('.graphml', '')
    return generate_topology2(G, topo)

def get_topology_graph():
    TOPOYML = f"{BASEDIR}/config/simulate_topo.yml"
    with open(TOPOYML, 'rb') as yml_file:
        topoconfig = yaml.load(yml_file, Loader=yaml.FullLoader)

    # Load information about the topology to test
    topo_name = topoconfig['to_test']
    details = topoconfig['topology'][topo_name]
    topo_func_name = topoconfig['topology'][topo_name]['func']
    topo_func = globals()[topo_func_name]

    G = topo_func(details)
    return G

if __name__ == '__main__':
    G = get_topology_graph()
    nx.write_graphml(G, f'{BASEDIR}/final_topology.xml')
