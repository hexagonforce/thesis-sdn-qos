"""
    JETR
"""
from ryu.lib.packet import ether_types

import pickle
import yaml
import os

def test_algo(event):
    msg = event.msg
    datapath = msg.datapath
    ofproto = datapath.ofproto
    parser = datapath.ofproto_parser
    in_port = msg.match['in_port']

    match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP)
    actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
    mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=10, match=match, instructions=inst)

    datapath.send_msg(mod)

def basic_cbq_leaves(event, switch, nodes_config, dest_port):
    ''' Basic Class-based queueing algorithm, enforced at the leaves
        It only does upstream requests and not downstream stuff at the moment
        because the implementation of everything else is actually retarded
    '''
    msg = event.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    in_port = msg.match['in_port']
    qos_port = switch['qos_port']

    # We don't enforce anything if it's not a leaf switch
    if not 'client-leaf' in switch['type']:
        test_algo(event)
    
    # We also don't enforce anything if the destination port is not the QoS Port
    if dest_port != qos_port:
        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id, in_port=in_port,
            actions=actions, data=msg.data)
        dp.send_msg(out)
        return

    # flow mods for the protocols we are testing (found in custom/traffic_class.conf)
    for trcls in nodes_config['traffic']:
        out_port = switch['qos_port']
        actions = [ofp_parser.OFPActionOutput(out_port), 
                                            ofp_parser.OFPActionSetQueue(
                                                queue_id=nodes_config['traffic'][trcls]['proto_queue_id'])]
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, 
                                    ip_proto=nodes_config['traffic'][trcls]['nwproto'], 
                                    tcp_dst=nodes_config['traffic'][trcls]['tpdst'])
        mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, 
                                    priority=nodes_config['traffic'][trcls]['proto_priority'], 
                                    match=match, instructions=inst, table_id=0)
        dp.send_msg(mod)

    # flow mods for all IP packets that are not using the protocols being tested
    last_queue_id = switch['queue_count'] - 1
    for server_entry in nodes_config['servers_list']:
        out_port = switch['qos_port']
        actions = [ofp_parser.OFPActionOutput(out_port), ofp_parser.OFPActionSetQueue(queue_id=last_queue_id)]
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, ipv4_dst=server_entry['ip'])
        # match2 = ofp_parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP)
        mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, priority=10,
                                    match=match, instructions=inst, table_id=0)
        dp.send_msg(mod)

def basic_cbq_core(event, switch, nodes_config):
    msg = event.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    in_port = msg.match['in_port']

    last_queue_id = switch['queue_count'] - 1
    for trcls in nodes_config['traffic']:
        out_port = switch['qos_port']
        actions = [ofp_parser.OFPActionOutput(out_port), 
                                            ofp_parser.OFPActionSetQueue(
                                                queue_id=nodes_config['traffic'][trcls]['proto_queue_id'])]
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, 
                                    ip_proto=nodes_config['traffic'][trcls]['nwproto'], 
                                    tcp_dst=nodes_config['traffic'][trcls]['tpdst'])
        mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, 
                                    priority=nodes_config['traffic'][trcls]['proto_priority'], 
                                    match=match, instructions=inst, table_id=1)

        dp.send_msg(mod)

    for server_entry in nodes_config['servers_list']:
        out_port = switch['qos_port']
        actions = [ofp_parser.OFPActionOutput(out_port), ofp_parser.OFPActionSetQueue(queue_id=last_queue_id)]
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, ipv4_dst=server_entry['ip'])
        mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, priority=10,
                                    match=match, instructions=inst, table_id=1)
        dp.send_msg(mod)
