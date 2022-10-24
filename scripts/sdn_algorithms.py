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

def add_flow(msg, dp, queue_id, nwproto, priority, in_port, out_port, eth_src, eth_dst):
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
        'ip_proto': nwproto
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

def basic_cbq_leaves(event, switch, nodes_config, eth_src, eth_dst, out_port):
    ''' 
    Basic Class-based queueing algorithm, enforced at the leaves
    '''
    msg = event.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    in_port = msg.match['in_port']
    
    # If it's not the leaf we don't apply any QoS flows
    if not 'client-leaf' in switch['type']:
        add_flow(msg, dp, None, None, 10, in_port, out_port, eth_src, eth_dst)
        add_flow(msg, dp, None, None, 10, out_port, in_port, eth_dst, eth_src)
    elif out_port != ofp.OFPP_FLOOD:
        for details in nodes_config['traffic'].values():
            queue_id = details['proto_queue_id']
            nwproto = details['nwproto']
            priority = details['proto_priority']
            add_flow(msg, dp, queue_id, nwproto, priority, in_port, out_port, eth_src, eth_dst)
            add_flow(msg, dp, queue_id, nwproto, priority, out_port, in_port, eth_dst, eth_src)

        add_flow(msg, dp, switch['queue_count']-1, None, 10, in_port, out_port, eth_src, eth_dst)
        add_flow(msg, dp, switch['queue_count']-1, None, 10, out_port, in_port, eth_dst, eth_src)

def basic_cbq_core(event, switch, nodes_config, eth_src, eth_dst, out_port):
    msg = event.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    in_port = msg.match['in_port']

    if not 'core' in switch['type']:
        add_flow(msg, dp, None, None, 10, in_port, out_port, eth_src, eth_dst)
        add_flow(msg, dp, None, None, 10, out_port, in_port, eth_dst, eth_src)
    elif out_port != ofp.OFPP_FLOOD:
        for details in nodes_config['traffic'].values():
            queue_id = details['proto_queue_id']
            nwproto = details['nwproto']
            priority = details['proto_priority']
            add_flow(msg, dp, queue_id, nwproto, priority, in_port, out_port, eth_src, eth_dst)
            add_flow(msg, dp, queue_id, nwproto, priority, out_port, in_port, eth_dst, eth_src)

        add_flow(msg, dp, switch['queue_count']-1, None, 10, in_port, out_port, eth_src, eth_dst)
        add_flow(msg, dp, switch['queue_count']-1, None, 10, out_port, in_port, eth_dst, eth_src)

