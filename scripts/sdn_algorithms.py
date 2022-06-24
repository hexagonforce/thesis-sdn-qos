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
    mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=5, match=match, instructions=inst)

    datapath.send_msg(mod)

def basic_cbq_leaves(event, switch, nodes_config, dest_eth, dest_port):
    ''' Basic Class-based queueing algorithm, enforced at the leaves
        It only does upstream requests and not downstream stuff at the moment
        because the implementation of everything else is actually retarded
    '''
    msg = event.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    in_port = msg.match['in_port']
    out_port = dest_port

    if not 'client-leaf' in switch['type']:
        test_algo(event)
    elif out_port == ofp.OFPP_FLOOD:
        out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=ofp.OFP_NO_BUFFER,
                                      in_port=in_port, actions=[ofp_parser.OFPActionOutput(dest_port)],
                                      data=msg.data)
        dp.send_msg(out)
    else:
        for trcls in nodes_config['traffic']:
            out_port = dest_port
            actions = [ofp_parser.OFPActionOutput(out_port), 
                                                ofp_parser.OFPActionSetQueue(
                                                    queue_id=nodes_config['traffic'][trcls]['proto_queue_id'])]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
            match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, eth_dst=dest_eth,
                                        ip_proto=nodes_config['traffic'][trcls]['nwproto'], 
                                        tcp_dst=nodes_config['traffic'][trcls]['tpdst'])
            mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, 
                                        priority=nodes_config['traffic'][trcls]['proto_priority'], 
                                        match=match, instructions=inst, table_id=0)
            dp.send_msg(mod)

        # flow mods for all IP packets that are not using the protocols being tested
        last_queue_id = switch['queue_count'] - 1
        actions = [ofp_parser.OFPActionOutput(out_port), ofp_parser.OFPActionSetQueue(queue_id=last_queue_id)]
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, eth_dst=dest_eth)
        mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, priority=10,
                                    match=match, instructions=inst, table_id=0)
        dp.send_msg(mod)

def basic_cbq_core(event, switch, nodes_config, dest_eth, dest_port):
    msg = event.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser
    in_port = msg.match['in_port']
    out_port = dest_port

    if not 'core' in switch['type']:
        test_algo(event)
    elif out_port == ofp.OFPP_FLOOD:
        out = ofp_parser.OFPPacketOut(datapath=dp, buffer_id=ofp.OFP_NO_BUFFER,
                                      in_port=in_port, actions=[ofp_parser.OFPActionOutput(dest_port)],
                                      data=msg.data)
        dp.send_msg(out)
    else:
        for trcls in nodes_config['traffic']:
            out_port = dest_port
            actions = [ofp_parser.OFPActionOutput(out_port), 
                                                ofp_parser.OFPActionSetQueue(
                                                    queue_id=nodes_config['traffic'][trcls]['proto_queue_id'])]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
            match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, eth_dst=dest_eth,
                                        ip_proto=nodes_config['traffic'][trcls]['nwproto'], 
                                        tcp_dst=nodes_config['traffic'][trcls]['tpdst'])
            mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, 
                                        priority=nodes_config['traffic'][trcls]['proto_priority'], 
                                        match=match, instructions=inst, table_id=0)
            dp.send_msg(mod)

        # flow mods for all IP packets that are not using the protocols being tested
        last_queue_id = switch['queue_count'] - 1
        actions = [ofp_parser.OFPActionOutput(out_port), ofp_parser.OFPActionSetQueue(queue_id=last_queue_id)]
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, eth_dst=dest_eth)
        mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, priority=10,
                                    match=match, instructions=inst, table_id=0)
        dp.send_msg(mod)