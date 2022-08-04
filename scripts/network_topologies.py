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

def add_edge(node1, node2, switch_port_num, adjlist, edgelist):
    '''
    adds an edge to the adjacency list and edgelist, and updates the switch port numbers accordingly.
    '''
    port1 = 0
    port2 = 0
    if (node1 in switch_port_num):
        switch_port_num[node1] += 1
        port1 = switch_port_num[node1]
    if (node2 in switch_port_num):
        switch_port_num[node2] += 1
        port2 = switch_port_num[node2]
    if (not node1 in adjlist):
        adjlist[node1] = {}
    if (not node2 in adjlist):
        adjlist[node2] = {}
    
    adjlist[node1][node2] = port1
    adjlist[node2][node1] = port2
    if (node1 > node2):
        node1, node2 = node2, node1
        port1, port2 = port2, port1
    edgelist.add((node1, node2, port1, port2))
    return switch_port_num, adjlist, edgelist

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

def fat_tree(topo):
    layers = topo['details']['leaf_switch_layers']
    fanout = topo['details']['fanout']
    topo['details']['client_switches'] = fanout ** layers
    topo['details']['core_switch_num'] = 1

    G = nx.balanced_tree(fanout, layers)
    return generate_topology(G, topo)

def mesh(topo):
    num_switches = topo['details']['switches']
    G = nx.complete_graph(num_switches)
    return generate_topology(G, topo)

def zoo_data(topo):
    filename = topo['details']['filename']
    filepath = f'{BASEDIR}/zoo_data/{filename}'
    G = nx.read_graphml(filepath)
    return generate_topology(G, topo)

def generate_topology(G, topo):

    if 'core_switch_num' in topo['details']:
        core_switch_num = int(topo['details']['core_switch_num'])
    else:
        core_switch_num = int(farthest_by_hops(G)) + 1

    num_switches = nx.number_of_nodes(G)
    num_client_switches = topo['details']['client_switches']
    if num_client_switches == 'max' or num_client_switches > num_switches - 1:
        num_client_switches = num_switches - 1
    num_clients = topo['details']['clients']

    list_clients = [f'client{x}' for x in range(1, num_clients + 1)]
    list_servers = [f'server{x}' for x in range(1, NUM_SERVERS + 1)]

    core_switch = f'switch{core_switch_num}'
    edge_switches = []
    internal_switches = []
    server_switch = f'switch{num_switches + 1}'

    for node in reversed(list(G.nodes)):
        nodenum = int(node) + 1
        if nodenum == core_switch_num:
            pass
        elif len(edge_switches) < num_client_switches:
            # by default, the nodes that will be connected to the clients are the nodes with the highest ids
            edge_switches.append(f'switch{nodenum}')
        else:
            internal_switches.append(f'switch{nodenum}')

    all_switches = edge_switches + internal_switches + [core_switch] + [server_switch]

    switch_port_num = {switch : 0 for switch in all_switches}
    adjlist = {}
    edgelist = set()
    
    edge_switches = sorted(edge_switches)
    client_ranges = divider(num_clients, num_client_switches)
    for idx, (prev, upper_bound) in enumerate(zip(client_ranges, client_ranges[1:])):
        for clientnum in range(prev + 1, upper_bound + 1):
            switch_port_num, adjlist, edgelist = add_edge(f'client{clientnum}', edge_switches[idx],
                                                switch_port_num, adjlist, edgelist)

    for u, v in nx.edges(G):
        switchu = f'switch{int(u)+1}'
        switchv = f'switch{int(v)+1}'
        add_edge(switchu, switchv, switch_port_num, adjlist, edgelist)

    # Connect the core switch (defined as the switch with the largest number) to the server_switch
    add_edge(core_switch, server_switch, switch_port_num, adjlist, edgelist)
    
    # add the servers to the server switch
    for server in list_servers:
        add_edge(server_switch, server, switch_port_num, adjlist, edgelist)

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
    return result

if __name__ == '__main__':
    TOPOYML = f"{BASEDIR}/config/simulate_topo.yml"
    with open(TOPOYML, 'rb') as yml_file:
        topoconfig = yaml.load(yml_file, Loader=yaml.FullLoader)

    # Load information about the topology to test
    topo_name = topoconfig['to_test']
    details = topoconfig['topology'][topo_name]
    topo_func_name = topoconfig['topology'][topo_name]['func']
    topo_func = globals()[topo_func_name]

    # Get the nodes and links information
    result = topo_func(details)
    result['topo_name'] = topo_name
    result['topo_details'] = details
    
    with open(f'{BASEDIR}/config/custom/topology_information.yml', 'w') as file:
        yaml.dump(result, file)