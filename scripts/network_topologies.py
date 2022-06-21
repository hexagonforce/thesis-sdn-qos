"""
    JETR
"""

import pickle
import yaml
import os
import json

BASEDIR = os.getcwd()
vhost_mapping = f"{BASEDIR}/pcap/vhost_mapping.json"

NUM_SERVERS = 6
def fat_tree(net, topo):
    """
    Generates a fat_tree topology
    net is a Mininet Object, and topo is the parsed YAML configuration file from simulate_topo.yml.
    Virtual host addresses are provided by pcap/vhost_mapping.json
    """
    def divider(clients, leaves):
        """
        Evenly divides the clients to the leaf switches and gives the 
        last client numbers per leaf (1 indexed)
        example: 70 Clients and 8 Leaves will result in 2 leaves with 8 clients and 6 leaves with 9 clients, therefore the output of 
        divider(70, 8) is [8, 16, 25, 34, 43, 52, 61, 70]
        
        """
        clients_per_leaf = clients // leaves
        remaining_clients = clients % leaves
        last_client_number_list = [clients_per_leaf]
        for i in range(1, leaves):
            if i == leaves - remaining_clients:
                clients_per_leaf += 1
            last_client_number_list.append(clients_per_leaf + last_client_number_list[-1])
            
        return last_client_number_list
    def switch_layers(layers, layer_1, switches, fanout):
        """
        layers: number of layers in the topology
        layer_1: number of switches in layer 1
        switches: map of switch numbers to the actual switch objects
        returns a dict whose keys are the layer numbers starting from layer 1 (the ones with the leaf switches)
        all the way up to layer `layers`, and whose values are the list of actual switch objects in that layer.
        """
        fat_tree = {}
        keys = list(switches.keys())
        switches_count = layer_1

        for i in range(1, layers+1):
            layer_switches = []
            for j in range(0, switches_count):
                switch_num = keys.pop(0)
                layer_switches.append(switches[switch_num])
            fat_tree[i] = layer_switches
            switches_count = switches_count // fanout

        return fat_tree

    ceil = topo['details']['clients']
    layers = topo['details']['leaf_switch_layers']
    fanout = topo['details']['fanout']
    total_switches = fanout ** (layers+1)
    leaf_switches_cnt = fanout ** layers
    ranges = divider (ceil, leaf_switches_cnt)
    index = 0

    # Add hosts and switches
    clients = {}
    for x in range(1, ceil+1):
        clients[x] = net.addHost('client%s' % x)
    server1 = net.addHost( 'server1', ip="10.0.1.101" ) # inNamespace=False
    server2 = net.addHost( 'server2', ip="10.0.1.102" ) 
    server3 = net.addHost( 'server3', ip="10.0.1.103" ) 
    server4 = net.addHost( 'server4', ip="10.0.1.104" ) 
    server5 = net.addHost( 'server5', ip="10.0.1.105" ) 
    server6 = net.addHost( 'server6', ip="10.0.1.106" )

    switches = {}
    for i in range(1, (total_switches+1)):
        # implement similar to clients
        switches[i] = net.addSwitch('switch%s' % i)

    # Add Links for First Layers
    # TODO: REWORK EVERYTHING UP TO LINE 108
    for i in  range (1, ceil+1):
        if i <= ranges[index]:
            net.addLink( clients[i], switches[index+1])
        else:
            index = index + 1
            net.addLink( clients[i], switches[index+1])
    
    fat_tree = switch_layers(layers, leaf_switches_cnt, switches, fanout)
    core_switch = switches[(int(fat_tree[layers][1].name.split('switch')[1])+1)]
    server_switch = switches[(int(fat_tree[layers][1].name.split('h')[1])+2)]

    for i in range(1, layers):
        ranges = divider(len(fat_tree[i]), len(fat_tree[i+1]))
        ranges.append(len(fat_tree[i])) # check this
        index = 0
        layer_min = int(fat_tree[i][0].name.split('h')[1])
        layer_max = int(fat_tree[i][len(fat_tree[i])-1].name.split('h')[1])

        for j in range(0, len(fat_tree[i])):
            if j < ranges[index]:
                net.addLink(switches[int(fat_tree[i][j].name.split('h')[1])], switches[int(fat_tree[i+1][index].name.split('h')[1])])
            else:
                index = index + 1
                net.addLink(switches[int(fat_tree[i][j].name.split('h')[1])], switches[int(fat_tree[i+1][index].name.split('h')[1])])

    # Add Link to Core Switch
    for switch in fat_tree[layers]:
        net.addLink(switch, core_switch)

    # Link Core Switch to Server Switch
    net.addLink(core_switch, server_switch)
    net.addLink( server_switch, server1 )
    net.addLink( server_switch, server2 )
    net.addLink( server_switch, server3 )
    net.addLink( server_switch, server4 )
    net.addLink( server_switch, server5 )
    net.addLink( server_switch, server6 )

def mesh(net, topo):
    num_switches = topo['details']['switches']
    num_client_switches = topo['details']['switches']
    num_clients = topo['details']['clients']
    assert(num_client_switches < num_clients)
    # Initialize all the clients and switches first
    list_clients = [net.addHost(f'client{x}') for x in range(1, num_clients + 1)]
    list_switches = [net.addSwitch(f'switch{x}') for x in range(1, num_switches + 1)]

    # Distribute all the clients equally among client_switches "leaf switches"
    clients_per_switch = num_clients // num_client_switches
    remaining_clients = num_clients % num_client_switches
    num_clients_for_each_switch = [clients_per_switch+1 if x < remaining_clients else clients_per_switch for x in range(num_client_switches)]
    client_index = 0
    for switch_index, x in enumerate(num_clients_for_each_switch):
        for i in range(x):
            net.addLink(list_clients[client_index], list_switches[switch_index])
            client_index += 1

    # Connect the core switch (defined as the switch with the largest number) to the server_switch
    core_switch = list_switches[-1]
    server_switch = net.addSwitch(f'switch{num_switches + 1}')
    net.addLink(core_switch, server_switch)

    # pairwise connect all the switches
    for a in list_switches:
        for b in list_switches:
            if a != b:
                net.addLink(a, b)
    # add the servers to the server switch
    for ip in range(1, NUM_SERVERS + 1):
        server = net.addHost(f'server{ip}', ip=f'10.0.1.{100 + ip}')
        net.addLink(server_switch, server)
    


def twoway_linear(net, topo):
    left_host = net.addHost('LeftHost')
    right_host = net.addHost('RightHost')

    left_switch = net.addSwitch('src1')
    right_switch = net.addSwitch('dst2')

    core_switch = net.addSwitch('cs3')

    print (f"\n\nLeft Switch: {int(left_switch.dpid)}\nRight Switch: {int(right_switch.dpid)}\nCore Switch: {int(core_switch.dpid)}\n\n")

    net.addLink(left_host, left_switch)
    net.addLink(right_host, right_switch)
    net.addLink(left_switch, right_switch)











