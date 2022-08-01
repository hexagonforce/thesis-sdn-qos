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

    match = parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP)
    actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
    mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=5, match=match, instructions=inst)

    datapath.send_msg(mod)

def basic_cbq_leaves(event, switch, nodes_config, eth_src, eth_dst, dest_port):
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
    # If it's not the leaf we don't apply any QoS flows
    if not 'client-leaf' in switch['type']:
        test_algo(event)
    elif out_port != ofp.OFPP_FLOOD:
        for details in nodes_config['traffic'].values():
            actions = [ofp_parser.OFPActionSetQueue(queue_id=details['proto_queue_id']),
                        ofp_parser.OFPActionOutput(out_port)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
            nwproto = details['nwproto']
            match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, 
                                    eth_src=eth_src, eth_dst=eth_dst,
                                    ip_proto=nwproto)
            mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, 
                                        priority=details['proto_priority'], 
                                        match=match, instructions=inst, table_id=0)

            dp.send_msg(mod)

        # flow mods for all IP packets that are not using the protocols being tested
        last_queue_id = switch['queue_count'] - 1
        actions = [ofp_parser.OFPActionSetQueue(queue_id=last_queue_id), ofp_parser.OFPActionOutput(out_port)]
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, eth_src=eth_src, eth_dst=eth_dst)
        mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, priority=10,
                                    match=match, instructions=inst, table_id=0)
        dp.send_msg(mod)

def basic_cbq_core(event, switch, nodes_config, eth_src, eth_dst, dest_port):
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
        for trcls, details in nodes_config['traffic'].items():
            actions = [ofp_parser.OFPActionSetQueue(queue_id=nodes_config['traffic'][trcls]['proto_queue_id']),
                        ofp_parser.OFPActionOutput(out_port)]
            inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
            match = None
            if details['nwproto'] == 6:
                match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, 
                                            eth_src=eth_src, eth_dst=eth_dst,
                                            ip_proto=6)
            elif details['nwproto'] == 17:
                match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP,
                                            eth_src=eth_src, eth_dst=eth_dst,
                                            ip_proto=17)
            mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, 
                                        priority=details['proto_priority'], 
                                        match=match, instructions=inst, table_id=0)

            dp.send_msg(mod)

        # flow mods for all IP packets that are not using the protocols being tested
        last_queue_id = switch['queue_count'] - 1
        actions = [ofp_parser.OFPActionOutput(out_port), ofp_parser.OFPActionSetQueue(queue_id=last_queue_id)]
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        match = ofp_parser.OFPMatch(in_port=in_port, eth_type=ether_types.ETH_TYPE_IP, eth_src=eth_src, eth_dst=eth_dst)
        mod = ofp_parser.OFPFlowMod(datapath=dp, buffer_id=msg.buffer_id, priority=10,
                                    match=match, instructions=inst, table_id=0)
        dp.send_msg(mod)