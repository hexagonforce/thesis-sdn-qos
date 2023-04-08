from scripts.custom.networkconfig import clients, hosts, load_conf, sourcequeue, switch_configs, ovs_qosgenerator
from util.constants import BASEDIR
from pathlib import Path
 
OUTDIR = BASEDIR / 'config/custom'

def generate_all_configs(G):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    clients.save_to_conf(OUTDIR, G)
    load_conf.save_to_conf(OUTDIR, G)
    sourcequeue.save_to_conf(OUTDIR, G)
    switch_configs.save_to_conf(OUTDIR, G)
    ovs_qosgenerator.save_to_conf(OUTDIR, G)
    hosts.save_to_conf(OUTDIR, G)
