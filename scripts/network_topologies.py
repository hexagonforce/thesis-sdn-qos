"""
    JETR
"""

import pickle
import yaml
import os
import json

BASEDIR = os.getcwd()
vhost_mapping = f"{BASEDIR}/pcap/vhost_mapping.json"

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

    def switch_layers(layers, layer_1, switches):
        """
        layers: number of layers in the topology
        layer_1: number of switches in layer 1
        switches: map of switch numbers to the actual switch objects
        returns a dict whose keys are the layer numbers starting from layer 1 (the ones with the leaf switches)
        all the way up to layer `layers`.
        """
        fat_tree = {}
        keys = list(switches.keys())
        switches_count = layer_1

        for i in range(1, layers+1):
            layer_switches = []
            for j in range(0, int(switches_count)):
                switch_num = keys.pop(0) # Get the first number
                layer_switches.append(switches[switch_num])
            fat_tree[i] = layer_switches
            switches_count = switches_count / 2

        return fat_tree

    print (net)
    print (topo)
    ceil = topo['details']['clients']
    layers = topo['details']['leaf_switch_layers']
    total_switches = 2 ** (layers+1)
    leaf_switches_cnt = 2 ** layers
    ranges = divider (ceil, leaf_switches_cnt)
    index = 0

    ip = 1

    with open(vhost_mapping, 'rb') as json_file:
        vhost_map = json.load(json_file)
        print (vhost_map)

    # start_host = net.addHost('host1')
    vhosts = {}
    for vhost in vhost_map:
        vhosts[vhost] = net.addSwitch(vhost)

    hosts = {}
    for vhost in vhosts:
        hosts[vhost] = net.addHost(f"host{vhost}", ip=f"10.0.0.{ip}")
        net.addLink(hosts[vhost], vhosts[vhost])
        ip += 1

    switches = {}
    for i in range(1, (total_switches+1)):
        switches[i] = net.addSwitch('switch%s' % i)

    for i in range(1, total_switches+1):
        if i <= ceil / 2:
            net.addLink(vhosts[f"vhost{i}"], switches[index+1])
        else:
            index = index + 1
            net.addLink(vhosts[f"vhost{i}"], switches[index+1])

    fat_tree = switch_layers(layers, leaf_switches_cnt, switches)
    print (fat_tree)
    core_switch = switches[(int(fat_tree[layers][1].name.split('switch')[1])+1)]

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

    end_host = net.addHost(f'host{ceil+1}', ip=f"10.0.0.{ip}")
    net.addLink(end_host, core_switch)

    return switches

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











