# This class is used exclusively by nodes_config.py to parse the config files
# and create lists of hosts and lists of switches.
# Refer to the node_classes.py for more information.

from .node_classes import Host
from .node_classes import Switch

def get_host_entries(host_entries):
    hosts_list = []
    clients_list = []
    servers_list = []
    for host_entry in host_entries:
        h_ip = host_entry
        h_name = ""
        h_switch_id=-1
        h_layer_switches = []
        h_port=-1
        h_is_server = False
        h_protocol = ""
        h_nwproto = -1
        h_tpdst = -1
        h_proto_priority = -1
        h_proto_queue_id = -1
        h_dst_queue_id = -1

        for host_entry_param in host_entries[host_entry]:
            param = host_entry_param.split("=")
            if len(param) >= 2:
                if param[0].strip() == "name":
                    h_name = param[1].strip()
                elif param[0].strip() == "switch":
                    try:
                        h_switch_id = int(param[1].strip())
                    except ValueError:
                        raise(ValueError)
                elif param[0].strip() == "port":
                    try:
                        h_port = int(param[1].strip())
                    except ValueError:
                        raise(ValueError)
                elif param[0].strip() == "protocol":
                    h_protocol = param[1].strip()
                elif param[0].strip() == "nwproto":
                    try:
                        h_nwproto = int(param[1].strip())
                    except ValueError:
                        raise(ValueError)
                elif param[0].strip() == "tpdst":
                    try:
                        h_tpdst = int(param[1].strip())
                    except ValueError:
                        raise(ValueError)
                elif param[0].strip() == "proto_priority":
                    try:
                        h_proto_priority = int(param[1].strip())
                    except ValueError:
                        raise(ValueError)
                elif param[0].strip() == "proto_queue_id":
                    try:
                        h_proto_queue_id = int(param[1].strip())
                    except ValueError:
                        raise(ValueError)
                elif param[0].strip() == "dst_queue_id":
                    try:
                        h_dst_queue_id = int(param[1].strip())
                    except ValueError:
                        raise(ValueError)
        if h_ip.strip() != "" and h_name != "" and h_switch_id > 0 and h_port > 0:
            if h_protocol != "" and h_nwproto > 0 and h_tpdst > 0:
                h_is_server = True
                servers_list.append(Host(ip=h_ip.strip(), name=h_name, switch_id=h_switch_id, 
                                                port=h_port, is_server=h_is_server, protocol=h_protocol, 
                                                nw_proto=h_nwproto, tp_dst=h_tpdst, proto_priority=h_proto_priority, 
                                                proto_queue_id = h_proto_queue_id, dst_queue_id=h_dst_queue_id))
            else:
                clients_list.append(Host(ip=h_ip.strip(), name=h_name, switch_id=h_switch_id, 
                                                port=h_port, is_server=h_is_server, protocol=h_protocol, 
                                                nw_proto=h_nwproto, tp_dst=h_tpdst, proto_priority=h_proto_priority, 
                                                proto_queue_id = h_proto_queue_id, dst_queue_id=h_dst_queue_id))
            hosts_list.append(Host(ip=h_ip.strip(), name=h_name, switch_id=h_switch_id, 
                                        port=h_port, is_server=h_is_server, protocol=h_protocol, 
                                        nw_proto=h_nwproto, tp_dst=h_tpdst, proto_priority=h_proto_priority))
    return hosts_list, clients_list, servers_list

def get_switch_entries(switches_entries, hosts_list, clients_list, servers_list):
    switches_list = {}
    for switch_entry in switches_entries:
        sw_id = -1
        try:
            sw_id = int(switch_entry.split('switch')[1])
        except ValueError as e:
            print ("ERROR: {}".format(e))

        sw_name = ""
        sw_dpid = ""
        sw_type = ""
        sw_core_port = -1
        sw_server_port = []
        sw_leaf_ports = []
        sw_queue_count = 0
        sw_qos_type = ""
        sw_qos_port = -1
        sw_hosts_entries = []

        for switch_entry_param in switches_entries[switch_entry]:
            param = switch_entry_param.split("=")
            # print ("\n\nparam: {}".format(param))
            if len(param) >= 2:
                if param[0].strip() == "name":
                    sw_name = param[1].strip()
                elif param[0].strip() == "dpid":
                    sw_dpid = param[1].strip()
                elif param[0].strip() == "type":
                    sw_type = param[1].strip()
                elif param[0].strip() == "queues":
                    try:
                        sw_queue_count = int(param[1].strip())
                    except ValueError:
                        raise(ValueError)
                elif param[0].strip() == "qos":
                    sw_qos_type = param[1].strip()

        if sw_id > 0 and sw_name != "" and sw_dpid != "" and sw_type != "":
            if sw_type == "core":
                sw_hosts_entries = hosts_list
            elif sw_type == "server-leaf":
                sw_hosts_entries = servers_list
            elif sw_type == "client-leaf":
                for client_entry in clients_list:
                    if sw_id == client_entry.switch_id:
                        sw_hosts_entries.append(client_entry)

            switches_list[sw_id] = Switch(id = sw_id, name = sw_name, dpid = sw_dpid, 
                                          type = sw_type, core_port = sw_core_port, server_port = sw_server_port, 
                                          leaf_ports = sw_leaf_ports, queue_count = sw_queue_count, qos_type = sw_qos_type, 
                                          qos_port = sw_qos_port, hosts_entries = sw_hosts_entries)

    return switches_list












































