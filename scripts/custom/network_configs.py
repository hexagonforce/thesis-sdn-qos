#JETR

#! /bin/python

# from networkconfig import range_divider
from networkconfig import clients, hosts, load_conf
from networkconfig import sourcequeue, switch_configs, ovs_qosgenerator
import os

OUTDIR = f"{os.getcwd()}/config/custom"
EXECDIR = f"{os.getcwd()}/scripts/custom"
clients.save_to_conf(OUTDIR) #
load_conf.save_to_conf(OUTDIR) #
# sourcequeue.save_to_conf(OUTDIR) # this needs dijkstra's
switch_configs.save_to_conf(OUTDIR)  #
ovs_qosgenerator.save_to_conf(OUTDIR, EXECDIR) #
hosts.save_to_conf(OUTDIR)



