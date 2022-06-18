"""
Emits a pkl/net_data/node_connections.pkl file that contains the shortest paths
between all the switches and all the clients.
"""

from networkconfig.graph import Graph

import os
import pickle
import yaml
import range_divider

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

BASEDIR = f"{os.getcwd()}"
yml = f"{BASEDIR}/config/simulate_topo.yml"
pkl = f"{BASEDIR}/pkl/net_data/node_connections.pkl"
print (f"PKL: {pkl}")

graph = Graph()

with open (yml, 'rb') as yml_file:
    topo = yaml.load(yml_file, Loader=yaml.FullLoader)

shortest_path_dict = {}
ceil = topo['topology']['fat_tree']['clients']
layers = topo['topology']['fat_tree']['leaf_switch_layers']
total_switches = 2 ** (layers+1)
layer_1 = 2 ** layers
ranges = range_divider.divider(ceil, layer_1)
fat_tree = range_divider.switch_layers()
keys = len(fat_tree.keys())
core_switch = int(fat_tree[keys][1].split('h')[1])+1
index = 0
edges = []

for i in range(1, ceil+1):
    if i <= ranges[index]:
        edges.append((f"client{i}", f"switch{index+1}", 1))
    else:
        index = index + 1
        edges.append((f"client{i}", f"switch{index+1}", 1))

for i in range(1, layers):
    ranges = range_divider.divider(len(fat_tree[i]), len(fat_tree[i+1]))
    index = 0
    layer_min = int(fat_tree[i][0].split('h')[1])
    layer_max = int(fat_tree[i][len(fat_tree[i])-1].split('h')[1])

    for j in range(0, len(fat_tree[i])):
        if j < ranges[index]:
            edges.append((fat_tree[i][j], fat_tree[i+1][index], 1))
        else:
            index = index+1
            edges.append((fat_tree[i][j], fat_tree[i+1][index], 1))

for switch in fat_tree[layers]:
    edges.append((switch, f"switch{core_switch}", 1))

for edge in edges:
    graph.add_edge(*edge)

for switch in range(layer_1+1, core_switch+1):
    for client in range(1, ceil+1):
        shortest_path_dict[f"switch{switch}:client{client}"] = int(dijsktra(graph, f"switch{switch}", f"client{client}")[1].split('switch')[1])


with open(pkl, 'wb') as pkl_file:
    # pickle.dump(config_data, pkl_file, pickle.HIGHEST_PROTOCOL)
    pickle.dump(shortest_path_dict, pkl_file, fix_imports=True, protocol=2) # , pickle.DEFAULT_PROTOCOL

for pair in shortest_path_dict:
    print (f"{pair} : {shortest_path_dict[pair]}")







