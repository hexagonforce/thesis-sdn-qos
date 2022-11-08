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

def add_flow(msg, queue_id, nwproto, tcp_src, tcp_dst, priority, in_port, out_port, eth_src, eth_dst):
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    actions = [
        ofp_parser.OFPActionSetQueue(queue_id=queue_id),
        ofp_parser.OFPActionOutput(out_port)
    ]
    if queue_id is None:
        actions = actions[1:]
    inst = [
        ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)
    ]
    match_args = {
        'in_port': in_port,
        'eth_type': ether_types.ETH_TYPE_IP,
        'eth_src': eth_src,
        'eth_dst': eth_dst,
        'ip_proto': nwproto,
        'tcp_src': tcp_src,
        'tcp_dst': tcp_dst
    } 
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
            nwproto = details.get('nwproto', None)
            priority = details.get('proto_priority', None)
            tcp_dst = details.get('tcp_dst', None)
            add_flow(msg, queue_id, nwproto, tcp_dst, None, priority, in_port, out_port, eth_src, eth_dst)
            add_flow(msg, queue_id, nwproto, None, tcp_dst, priority, in_port, out_port, eth_src, eth_dst)
            add_flow(msg, queue_id, nwproto, tcp_dst, None, priority, out_port, in_port, eth_dst, eth_src)
            add_flow(msg, queue_id, nwproto, None, tcp_dst, priority, out_port, in_port, eth_dst, eth_src)
        add_flow(msg, switch['queue_count']-1, None, None, None, 10, in_port, out_port, eth_src, eth_dst)
        add_flow(msg, switch['queue_count']-1, None, None, None, 10, out_port, in_port, eth_dst, eth_src)
    else:
        # flood_algo(event)
        add_flow(msg, 0, None, None, None, 1000, in_port, out_port, eth_src, eth_dst)
        add_flow(msg, 0, None, None, None, 1000, out_port, in_port, eth_dst, eth_src)

def basic_cbq_core(event, switch, nodes_config, out_port):
    basic_cbq(event, switch, nodes_config, out_port, 'core')

def basic_cbq_leaves(event, switch, nodes_config, out_port):
    basic_cbq(event, switch, nodes_config, out_port, 'client-leaf')