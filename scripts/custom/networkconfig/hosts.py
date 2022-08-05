# Generates hosts.conf which contains information about server and client hosts
# - name: the name of the host
# - switch: the switch that the host is connected to
# - port: the port of the switch that the host is connected to
# Server:
# 	- protocol: the protocol that the server responds to
#	- nwproto: the IP Protocol that the server uses (6 = TCP)
#	- tpdst: the destination port
# 	- proto_priority: the priority of the protocol (higher means more prioritized)
# 	- proto_queue_id: no idea

NUMBER_OF_SERVERS = 6

def dpid(node):
    return int(''.join(c for c in node if c.isdigit()))

def generate_conf(i, switch, port):
    return f"10.0.0.{i}\tname=client{i}\tswitch={switch}\tport={port}\n"

def generate_server(i, switch, port, protocol, tpdst, priority, proto_queue_id, dst_queue_id):
    return f"10.0.1.{100 + i}\tname=server{i}\tswitch={switch}\tport={port}\tprotocol={protocol}\tnwproto=6\ttpdst={tpdst}\tproto_priority={priority}\tproto_queue_id={proto_queue_id}\tdst_queue_id={dst_queue_id}\n"

def save_to_conf(basedir, G):
    config_file = open(f"{basedir}/hosts.conf", "w")

    server_switch = G.graph['server_switch']
    list_clients = [node for node, data in G.nodes(data='type') if data=='client']
    list_servers = [node for node, data in G.nodes(data='type') if data=='server']
    
    for client in list_clients:
        i = dpid(client)
        for switch in G[client]: # client is always less than switch
            port = G[client][switch]['rport']
            config_file.write(generate_conf(i, dpid(switch), port))
    
    for server in list_servers:
        i = dpid(server)
        for switch in G[server]: # same here, server always less than switch
            port = G[server][switch]['rport']
            if i % 2 == 0:
                config_file.write(generate_server(i, dpid(server_switch), port, 'vlc', 5004, 1000, 1, i-1))
            else:
                config_file.write(generate_server(i, dpid(server_switch), port, 'http', 80, 100, 0, i-1))





















