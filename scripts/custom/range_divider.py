import os
import yaml

BASEDIR = f"{os.getcwd()}/config/custom"

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

def switch_layers():
    switches = {}
    fat_tree = {}
    yml = f"{BASEDIR.split('custom')[0]}/simulate_topo.yml"
    with open (yml, 'rb') as yml_file:
        topo = yaml.load(yml_file, Loader=yaml.FullLoader)

    ceil = topo['topology']['fat_tree']['clients']
    layers = topo['topology']['fat_tree']['leaf_switch_layers']
    total_switches = 2 ** (layers+1)
    layer_1 = 2 ** layers
    for i in range(1, total_switches+1):
        switches[i] = 'switch{}'.format(i)

    keys = list(switches.keys())
    switches_count = int(layer_1)

    for i in range(1, layers+1):
        layer_switches = []
        for j in range(0, switches_count):
            switch_num = keys.pop(0)
            layer_switches.append(switches[switch_num])
        fat_tree[i] = layer_switches
        switches_count = int(switches_count / 2)

    return fat_tree






