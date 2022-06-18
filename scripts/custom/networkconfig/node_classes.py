#!/bin/python

# Value-object class for "Switch"
class Switch:
    def __init__ (self, id = -1, name = "", dpid = "", type = "", core_port = -1, server_port = -1, leaf_ports = [], queue_count = 0, qos_type = "", qos_port = -1, hosts_entries = []):
        self.id = id
        self.name = name
        self.dpid = dpid
        self.type = type
        self.core_port = core_port
        self.server_port = server_port
        self.leaf_ports = leaf_ports
        self.queue_count = queue_count
        self.qos_type = qos_type
        self.qos_port = qos_port
        self.hosts_entries = hosts_entries
        self.comments = ""
    
    def __str__(self):
        return','.join([str(self.id), self.name, str(self.dpid),
        				self.type, str(self.core_port), str(self.server_port),
        				str(self.leaf_ports), str(self.queue_count), self.qos_type, 
        				str(self.qos_port), str(self.hosts_entries), self.comments, "\n"])

    def __repr__(self):
        return','.join([str(self.id), self.name, str(self.dpid), 
        				self.type, str(self.core_port), str(self.server_port), 
        				str(self.leaf_ports), str(self.queue_count), self.qos_type, 
        				str(self.qos_port), str(self.hosts_entries), self.comments, "\n"])

# Value-object class for "Host"
class Host:
    def __init__ (self, ip, name, switch_id, port = -1, is_server = False, protocol = "", nw_proto = -1, tp_dst = -1, proto_priority = -1, proto_queue_id = -1, dst_queue_id = -1): # , dst_queue_id = -1
        self.ip = ip
        self.name = name
        self.switch_id = switch_id
        self.port = port
        self.is_server = is_server
        self.protocol = protocol
        self.nw_proto = nw_proto
        self.tp_dst = tp_dst
        self.proto_priority = proto_priority
        self.proto_queue_id = proto_queue_id
        self.dst_queue_id = dst_queue_id
    
    def __str__(self):
        return','.join([self.ip, self.name, str(self.switch_id), 
        				str(self.port), str(self.is_server), self.protocol, 
        				str(self.nw_proto), str(self.tp_dst), str(self.proto_priority), 
        				str(self.proto_queue_id), str(self.dst_queue_id),"\n"]) # , str(self.dst_queue_id)

    def __repr__(self):
        return','.join([self.ip, self.name, str(self.switch_id), 
        				str(self.port), str(self.is_server), self.protocol, 
        				str(self.nw_proto), str(self.tp_dst), str(self.proto_priority), 
        				str(self.proto_queue_id), str(self.dst_queue_id),"\n"]) # , str(self.dst_queue_id)





        