#*************************************************************
# Description: Python Program for initiating test execution.
# Filename   : executeTest.py
# Author     : O. V. Chato
# Execution  : To be run mininet interpreter command prompt.
#*************************************************************
#!/usr/bin/python

# from mininet.log import lg, info
# from mininet.net import Mininet
# import ConfigSetup
import time
import os.path, os, sys
import pwd
import logging
import grp
from datetime import date, datetime, timedelta
import csv
import yaml
import pickle
import pyshark

from scapy.all import *

logging.basicConfig(level=logging.DEBUG,
                    filename='execute.log', 
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')


global pkt_seq
pkt_seq = 0

def pkt_callback(pkt):
    # pkt.show()
    global pkt_seq
    pkt_seq = pkt_seq + 1
    print (pkt_seq)

sniff(iface="src1-eth1", prn=pkt_callback)


        