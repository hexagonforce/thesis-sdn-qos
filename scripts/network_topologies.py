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

    def divider(clients, leaves):
        divs = int(float(clients)/float(leaves))
        rng = 0
        rng_list = []
        for i in range(1, leaves):
            rng = rng + divs
            if rng <= clients:
                rng_list.append(rng)

        if len(rng_list) < leaves:
            for i in range(0, leaves-len(rng_list)):
                if (rng_list[len(rng_list)-1] + divs) <= clients:
                    rng_list.append(rng_list[len(rng_list)-1] + divs)

        if rng_list[len(rng_list)-1] < clients:
            diff = clients - rng_list[len(rng_list)-1]
            start = len(rng_list) - diff
            rng_list[len(rng_list)-1] = clients
            for i in range(start, len(rng_list)-1):
                rng_list[i] = rng_list[i-1] + (divs + 1)

        return rng_list

    def switch_layers(layers, layer_1, switches):
        fat_tree = {}
        keys = list(switches.keys())
        switches_count = layer_1

        for i in range(1, layers+1):
            layer_switches = []
            for j in range(0, int(switches_count)):
                switch_num = keys.pop(0)
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











