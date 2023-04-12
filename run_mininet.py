###
# This module takes a NetworkX graph
# adds all the nodes, hosts and links accordingly.
###

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
import networkx as nx

import yaml
import os

def dpid(node):
    return int(''.join((c for c in node if c.isdigit())))

def start_mininet_from_networkx_graph(G):
    net = Mininet(controller=RemoteController, autoSetMacs=True)

    net.addController('c0', controller=RemoteController)

    for node in G:
        if node.startswith('switch'):
            net.addSwitch(node, protocols=["OpenFlow13"])
        elif node.startswith('client'):
            net.addHost(node, ip=f'10.0.0.{dpid(node)}')
        elif node.startswith('server'):
            net.addHost(node, ip=f'10.0.1.{dpid(node) + 100}')

    for u, v, data in G.edges(data=True):
        net.addLink(min(u, v), max(u, v), data['lport'], data['rport'])
    net.start()
    return net

