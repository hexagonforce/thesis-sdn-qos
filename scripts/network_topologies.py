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

BASEDIR = os.getcwd()
NUM_SERVERS = 6

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

def fat_tree(topo):
    """
    Generates a fat_tree topology
    Arguments: topo is the parsed YAML configuration file from simulate_topo.yml.
    Outputs: config/custom/topology_information.yml
    Format: edges are the tuple (node1, node2, port1, port2)
    """
    # parameters from the file
    num_clients = topo['details']['clients']
    layers = topo['details']['leaf_switch_layers']
    fanout = topo['details']['fanout']

    num_total_switches = (fanout ** (layers+1) - 1) // (fanout - 1) # Sum of geometric series
    num_edge_switches = fanout ** layers # Last layer
    num_internal_switches = num_total_switches - num_edge_switches - 1

    # The graph
    core_switch = 'switch1'
    internal_switches = [f'switch{x}' for x in range(2, num_internal_switches + 2)]
    edge_switches = [f'switch{x}' for x in range(num_internal_switches + 2, num_total_switches + 1)]
    server_switch = f'switch{num_total_switches + 1}'

    list_clients = [f'client{x}' for x in range(1, num_clients + 1)]
    list_servers = [f'server{x}' for x in range(1, NUM_SERVERS + 1)]
    
    switch_port_num = {switch : 0 for switch in [f'switch{x}' for x in range(1, num_total_switches + 2)]}
    adjlist = {}
    edgelist = set()

    #add all the edge switch - client connections
    client_ranges = divider(num_clients, num_edge_switches)
    for idx, (prev, upper_bound) in enumerate(zip(client_ranges, client_ranges[1:])):
        for clientnum in range(prev + 1, upper_bound + 1):
            switch_port_num, adjlist, edgelist = add_edge(f'client{clientnum}', edge_switches[idx],
                                                switch_port_num, adjlist, edgelist)
    
    #add all the tree edges
    for parent_num in range(1, num_internal_switches + 2):
        childstart = (parent_num - 1) * fanout + 1 + 1
        for child_num in range(childstart, childstart + fanout):
            switch_port_num, adjlist, edgelist = add_edge(f'switch{parent_num}', f'switch{child_num}',
                                                switch_port_num, adjlist, edgelist)

    switch_port_num, adjlist, edgelist = add_edge(core_switch, server_switch, switch_port_num, adjlist, edgelist)
    
    for server in list_servers:
        switch_port_num, adjlist, edgelist = add_edge(server_switch, server, switch_port_num, adjlist, edgelist)

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

def mesh(topo):
    num_switches = topo['details']['switches']
    num_client_switches = topo['details']['client-switches']
    num_clients = topo['details']['clients']
    assert(num_client_switches < num_switches)

    # Initialize all the clients and switches first
    list_clients = [f'client{x}' for x in range(1, num_clients + 1)]
    list_switches = [f'switch{x}' for x in range(1, num_switches)]
    list_servers = [f'server{x}' for x in range(1, NUM_SERVERS + 1)]
    list_edges = []

    core_switch = list_switches[-1]
    server_switch = f'switch{num_client_switches + 1}'

    switch_ports = {switch : 0 for switch in list_switches}
    switch_ports[server_switch] = 0

    # Distribute all the clients equally among client_switches "leaf switches"
    clients_per_switch = num_clients // num_client_switches
    remaining_clients = num_clients % num_client_switches
    num_clients_for_each_switch = [clients_per_switch+1 if x < remaining_clients else clients_per_switch for x in range(num_client_switches)]
    
    client_index = 0
    for switch_index, x in enumerate(num_clients_for_each_switch):
        for i in range(x):
            switch = list_switches[switch_index]
            client = list_clients[client_index]
            switch_ports[switch] += 1
            list_edges.add((switch, client, switch_ports[switch], 0))
            client_index += 1

    # pairwise connect all the switches
    for a in list_switches:
        for b in list_switches:
            if a != b:
                switch_ports[a] += 1
                switch_ports[b] += 1
                list_edges.append((a, b, switch_ports[a], switch_ports[b]))

    # Connect the core switch (defined as the switch with the largest number) to the server_switch
    switch_ports[core_switch] += 1
    switch_ports[server_switch] += 1
    list_edges.append((core_switch, server_switch, switch_ports[core_switch], switch_ports[server_switch]))
    
    # add the servers to the server switch
    for server in list_servers:
        switch_ports[server_switch] += 1
        list_edges.append((server_switch, server, switch_ports[server_switch], 0))
    
    leaf_switches = list_switches[:num_client_switches]
    internal_switches = list_switches[num_client_switches:num_switches-1]

if __name__ == '__main__':
    TOPOYML = f"{BASEDIR}/config/simulate_topo.yml"
    with open(TOPOYML, 'rb') as yml_file:
        topo = yaml.load(yml_file, Loader=yaml.FullLoader)
    [[topo_name, details]] = topo['topology'].items()
    topo_func = globals()[topo_name]
    result = topo_func(details)
    with open(f'{BASEDIR}/config/custom/topology_information.yml', 'w') as file:
        yaml.dump(result, file)