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
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu import cfg

from scripts import sdn_algorithms

import logging, time, sys
import csv, operator, os 
import pickle, yaml, json

sys.modules['sdn_algorithms'] = sdn_algorithms

BASEDIR = os.getcwd()
USECASE_YML = f"{BASEDIR}/config/class_profile_functionname.yml"

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    """ The starting point for testing the QoS Algorithms
    Attributes:
    case: The case number loaded from the config file
    usecases: Class profiles loaded from the USECASE_YML directory. Class profile contain cases with their associated QoS Algorithms.
    algo: The QOS algorithm being tested (Write the algorithms in sdn_algorithms.py)
    """
    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.name = "Josiah Eleazar Regencia"

        CONF = cfg.CONF
        CONF.register_opts([
            cfg.StrOpt("case", default="0")])

        self.case = CONF.case.replace("\"", "")

        # self.usecase_yml = f"{BASEDIR}/config/class_profile_functionname.yml"

        with open(USECASE_YML, "rb") as yml_file:
            self.usecases = yaml.load(yml_file, Loader=yaml.FullLoader)['class_profiles']

        if self.case == self.usecases:
            self.logger.info(self.usecases[self.usecase]['description'])

        self.logger.info(f"Usecases: {self.usecases}")
        self.logger.info(f"Usecase: {self.case}")

        self.usecase_func_pkl = f"{BASEDIR}/pkl/algo/usecase_{self.case}_{self.usecases[self.case]['func_name']}_qosprotocol.pkl"

        with open(self.usecase_func_pkl, 'rb') as func_pkl:
            self.algo = pickle.load(func_pkl)

        nodes_config_filepath = f"{BASEDIR}/config/custom/usecase_{self.case}_nodes_configuration.json"
        with open(nodes_config_filepath, 'r') as nodes_config_file:
            self.nodes_configuration = json.load(nodes_config_file)
            self.switches_list = self.nodes_configuration['switches_list']
        self.mac_to_port = {}


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

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        in_port = msg.match['in_port']
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            dest_port = self.mac_to_port[dpid][dst]
        else:
            dest_port = ofproto.OFPP_FLOOD

        # If it's an ARP or a LLDP packet then just flood everywhere
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_ARP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=10, match=match, instructions=inst)

        datapath.send_msg(mod)

        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_LLDP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, buffer_id=msg.buffer_id, priority=10, match=match, instructions=inst)

        datapath.send_msg(mod)

        # If it's an IP packet then actually go to the correct queue in the correct port
        # print(f"packet_in event from switch{datapath.id}")
        messaging_switch = self.switches_list[str(datapath.id)]
        self.algo(ev, messaging_switch, self.nodes_configuration, dest_port)





























