# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import dpid as dpid_lib
from ryu.lib import stplib
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu import cfg
from ryu.app import simple_switch_13

from scripts import sdn_algorithms

import logging, time, sys
import csv, operator, os 
import pickle, yaml, json

sys.modules['sdn_algorithms'] = sdn_algorithms

BASEDIR = os.getcwd()
USECASE_YML = f"{BASEDIR}/config/class_profile_functionname.yml"


class QoSSwitch13(simple_switch_13.SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'stplib': stplib.Stp}
    """ The starting point for testing the QoS Algorithms
    Attributes:
    case: The case number loaded from the config file
    usecases: Class profiles loaded from the USECASE_YML directory. Class profile contain cases with their associated QoS Algorithms.
    algo: The QOS algorithm being tested (Write the algorithms in sdn_algorithms.py)
    """
    def __init__(self, *args, **kwargs):
        super(QoSSwitch13, self).__init__(*args, **kwargs)
        self.name = "Hyeong Seon Yoo"

        CONF = cfg.CONF
        CONF.register_opts([
            cfg.StrOpt("case", default="0"),
            cfg.StrOpt("core_switch", default="switch1")
        ])

        self.case = CONF.case.replace("\"", "")
        core_switch = CONF.core_switch.replace("\"", "")
        core_switch_num = ''.join((c for c in core_switch if c.isdigit()))

        with open(USECASE_YML, "rb") as yml_file:
            self.usecases = yaml.load(yml_file, Loader=yaml.FullLoader)['class_profiles']
        self.algo = getattr(sdn_algorithms, self.usecases[self.case]['func_name'])

        nodes_config_filepath = f"{BASEDIR}/config/custom/usecase_{self.case}_nodes_configuration.json"
        with open(nodes_config_filepath, 'r') as nodes_config_file:
            self.nodes_configuration = json.load(nodes_config_file)
            self.switches_list = self.nodes_configuration['switches_list']
        self.nodes_configuration
        self.mac_to_port = {}
        self.stp = kwargs['stplib']
        config = {dpid_lib.str_to_dpid(core_switch_num.zfill(16)):
                    {'bridge': {'priority': 0x8000}},
                 }
        self.stp.set_config(config)

    def delete_flow(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        for dst in self.mac_to_port[datapath.id].keys():
            match = parser.OFPMatch(eth_dst=dst)
            mod = parser.OFPFlowMod(
                datapath, command=ofproto.OFPFC_DELETE,
                out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
                priority=1, match=match)
            datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    @set_ev_cls(stplib.EventPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)

        dst = eth_pkt.dst
        src = eth_pkt.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            dest_port = self.mac_to_port[dpid][dst]
        else:
            dest_port = ofproto.OFPP_FLOOD

        # Installing the flow
    
        # If it's an ARP or a LLDP packet then just flood everywhere
        messaging_switch = self.switches_list[str(datapath.id)]

        last_queue_of_switch = messaging_switch['queue_count']
        if last_queue_of_switch > 0:
            last_queue_of_switch -= 1

        match_arp = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_ARP)
        match_lldp = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_LLDP)
        actions = [parser.OFPActionSetQueue(queue_id=last_queue_of_switch), parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=10, match=match_arp, instructions=inst)
        mod2 = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=10, match=match_lldp, instructions=inst)
        datapath.send_msg(mod)
        datapath.send_msg(mod2)

        #If it's an IP packet, install flows if we know the port
    
        self.algo(ev, messaging_switch, self.nodes_configuration, src, dst, dest_port)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
        in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    @set_ev_cls(stplib.EventTopologyChange, MAIN_DISPATCHER)
    def _topology_change_handler(self, ev):
        dp = ev.dp
        dpid_str = dpid_lib.dpid_to_str(dp.id)
        msg = 'Receive topology change event. Flush MAC table.'
        # self.logger.debug("[dpid=%s] %s", dpid_str, msg)

        if dp.id in self.mac_to_port:
            self.delete_flow(dp)
            del self.mac_to_port[dp.id]

    @set_ev_cls(stplib.EventPortStateChange, MAIN_DISPATCHER)
    def _port_state_change_handler(self, ev):
        dpid_str = dpid_lib.dpid_to_str(ev.dp.id)
        of_state = {stplib.PORT_STATE_DISABLE: 'DISABLE',
                    stplib.PORT_STATE_BLOCK: 'BLOCK',
                    stplib.PORT_STATE_LISTEN: 'LISTEN',
                    stplib.PORT_STATE_LEARN: 'LEARN',
                    stplib.PORT_STATE_FORWARD: 'FORWARD'}
        # self.logger.debug("[dpid=%s][port=%d] state=%s",
                          # dpid_str, ev.port_no, of_state[ev.port_state])
