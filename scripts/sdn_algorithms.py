from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import tcp
from ryu.lib.packet import ether_types

import pickle
import yaml
import os

def flood_algo(event):
    msg = event.msg
    datapath = msg.datapath
    ofproto = datapath.ofproto
    parser = datapath.ofproto_parser
    in_port = msg.match['in_port']

    match = parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP)
    actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
    mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=5, match=match, instructions=inst)

    datapath.send_msg(mod)

def filter_args(arg_dict):
    res = {}
    for k, v in arg_dict.items():
        if v is not None:
            res[k] = v
    return res

def add_flow(msg, queue_id, out_port, match_args, priority):
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser

    actions = [ofp_parser.OFPActionOutput(out_port)]
    if queue_id:
        actions = [ofp_parser.OFPActionSetQueue(queue_id=queue_id)] + actions

    inst = [
        ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)
    ]

    match = ofp_parser.OFPMatch(
        **filter_args(match_args)
    )
    mod_args = {
        'datapath': dp,
        'buffer_id': msg.buffer_id,
        'priority': priority,
        'match': match,
        'instructions': inst,
        'table_id': 0
    }
    mod = ofp_parser.OFPFlowMod(
        **filter_args(mod_args)
    )
    dp.send_msg(mod)

def basic_cbq(event, switch, nodes_config, out_port, mode):
    ''' 
    Basic Class-based queueing algorithm
    '''
    msg = event.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    
    in_port = msg.match['in_port']
    pkt = packet.Packet(msg.data)
    eth_pkt = pkt.get_protocol(ethernet.ethernet)
    eth_dst = eth_pkt.dst
    eth_src = eth_pkt.src

    # If it is the desired switch type, we apply the QoS rules.
    if mode in switch['type']:
        for details in nodes_config['traffic'].values():
            queue_id = details.get('proto_queue_id', None)
            ip_proto = details.get('nwproto', None)
            priority = details.get('proto_priority', None)
            tcp_dst = details.get('tcp_dst', None)
            flow1_args = {
                'in_port': in_port,
                'eth_type': ether_types.ETH_TYPE_IP,
                'eth_src': eth_src,
                'eth_dst': eth_dst,
                'ip_proto': ip_proto,
                'tcp_src': tcp_dst,
                'tcp_dst': None
            }
            flow2_args = {
                'in_port': in_port,
                'eth_type': ether_types.ETH_TYPE_IP,
                'eth_src': eth_src,
                'eth_dst': eth_dst,
                'ip_proto': ip_proto,
                'tcp_src': None,
                'tcp_dst': tcp_dst
            }
            flow3_args = {
                'in_port': out_port,
                'eth_type': ether_types.ETH_TYPE_IP,
                'eth_src': eth_dst,
                'eth_dst': eth_src,
                'ip_proto': ip_proto,
                'tcp_src': tcp_dst,
                'tcp_dst': None
            }
            flow4_args = {
                'in_port': out_port,
                'eth_type': ether_types.ETH_TYPE_IP,
                'eth_src': eth_dst,
                'eth_dst': eth_src,
                'ip_proto': ip_proto,
                'tcp_src': None,
                'tcp_dst': tcp_dst
            }
            add_flow(msg=msg, queue_id=queue_id, out_port=out_port, match_args=flow1_args, priority=priority)
            add_flow(msg=msg, queue_id=queue_id, out_port=out_port, match_args=flow2_args, priority=priority)
            add_flow(msg=msg, queue_id=queue_id, out_port=in_port, match_args=flow3_args, priority=priority)
            add_flow(msg=msg, queue_id=queue_id, out_port=in_port, match_args=flow4_args, priority=priority)
        flow5_args = {
            'in_port': in_port,
            'eth_type': ether_types.ETH_TYPE_IP,
            'eth_src': eth_src,
            'eth_dst': eth_dst
        }
        flow6_args = {
            'in_port': out_port,
            'eth_type': ether_types.ETH_TYPE_IP,
            'eth_src': eth_dst,
            'eth_dst': eth_src
        }
        add_flow(msg=msg, queue_id=switch['queue_count']-1, out_port=out_port, match_args=flow5_args, priority=1)
        add_flow(msg=msg, queue_id=switch['queue_count']-1, out_port=in_port, match_args=flow6_args, priority=1)
    else:
        flow7_args = {
            'in_port': in_port,
            'eth_type': ether_types.ETH_TYPE_IP,
            'eth_src': eth_src,
            'eth_dst': eth_dst
        }
        flow8_args = {
            'in_port': out_port,
            'eth_type': ether_types.ETH_TYPE_IP,
            'eth_src': eth_dst,
            'eth_dst': eth_src
        }
        add_flow(msg=msg, queue_id=0, out_port=out_port, match_args=flow7_args, priority=1000)
        add_flow(msg=msg, queue_id=0, out_port=in_port, match_args=flow8_args, priority=1000)

def basic_cbq_core(event, switch, nodes_config, out_port):
    basic_cbq(event, switch, nodes_config, out_port, 'core')

def basic_cbq_leaves(event, switch, nodes_config, out_port):
    basic_cbq(event, switch, nodes_config, out_port, 'client-leaf')

def source_cbq(event, switch, nodes_config, out_port, mode):
    msg = event.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    
    in_port = msg.match['in_port']
    pkt = packet.Packet(msg.data)
    eth_pkt = pkt.get_protocol(ethernet.ethernet)
    eth_dst = eth_pkt.dst
    eth_src = eth_pkt.src

    if mode in switch['type']:
        for source, queue_id in nodes_config['source'].items():
            queue_id = int(queue_id)
            flow1_args = {
                'in_port': in_port,
                'eth_type': ether_types.ETH_TYPE_IP,
                'eth_src': eth_src,
                'eth_dst': eth_dst,
                'ipv4_src': source
            }
            flow2_args = {
                'in_port': out_port,
                'eth_type': ether_types.ETH_TYPE_IP,
                'eth_src': eth_src,
                'eth_dst': eth_dst,
                'ipv4_dst': source
            }
            add_flow(msg=msg, queue_id=queue_id, priority=100, match_args=flow1_args, out_port=out_port)
            add_flow(msg=msg, queue_id=queue_id, priority=100, match_args=flow1_args, out_port=in_port)
        flow3_args = {
            'in_port': in_port,
            'eth_type': ether_types.ETH_TYPE_IP,
            'eth_src': eth_src,
            'eth_dst': eth_dst,
        }
        flow4_args = {
            'in_port': out_port,
            'eth_type': ether_types.ETH_TYPE_IP,
            'eth_src': eth_src,
            'eth_dst': eth_dst,
        }
        add_flow(msg=msg, queue_id=switch['queue_count']-1, priority=1, match_args=flow3_args, out_port=out_port)
        add_flow(msg=msg, queue_id=switch['queue_count']-1, priority=1, match_args=flow4_args, out_port=in_port)
    else:
        flow5_args = {
            'in_port': in_port,
            'eth_type': ether_types.ETH_TYPE_IP,
            'eth_src': eth_src,
            'eth_dst': eth_dst
        }
        flow6_args = {
            'in_port': out_port,
            'eth_type': ether_types.ETH_TYPE_IP,
            'eth_src': eth_dst,
            'eth_dst': eth_src
        }
        add_flow(msg=msg, out_port=out_port, queue_id=0, match_args=flow5_args, priority=1000)
        add_flow(msg=msg, out_port=in_port, queue_id=0, match_args=flow6_args, priority=1000)

def source_cbq_core(event, switch, nodes_config, out_port):
    source_cbq(event, switch, nodes_config, out_port, 'core')

def source_cbq_leaves(event, switch, nodes_config, out_port):
    source_cbq(event, switch, nodes_config, out_port, 'client-leaf')
