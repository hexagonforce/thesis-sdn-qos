from .networkconfig import clients, hosts, load_conf, sourcequeue, switch_configs, ovs_qosgenerator
import os

OUTDIR = f"{os.getcwd()}/config/custom"

def generate_all_configs(G):
    clients.save_to_conf(OUTDIR, G)
    load_conf.save_to_conf(OUTDIR, G)
    sourcequeue.save_to_conf(OUTDIR)
    switch_configs.save_to_conf(OUTDIR, G)
    ovs_qosgenerator.save_to_conf(OUTDIR, G)
    hosts.save_to_conf(OUTDIR, G)
