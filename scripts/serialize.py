# This file outputs pickle files to pkl/algo and pkl/topo
# by reading the relevant configurations from config/class_profile_functionname.yml
# and config/topology_definitions.yml

from sdn_algorithms import *

BASEDIR = os.getcwd()
QOS_OUTDIR = f"{BASEDIR}/pkl/algo"
qos_yml = f"{BASEDIR}/config/class_profile_functionname.yml"

with open(qos_yml, 'rb') as yml_file:
    yml_data = yaml.load(yml_file) # , Loader=yaml.FullLoader

for case in yml_data['class_profiles']:
    pkl = f"{QOS_OUTDIR}/usecase_{case}_{yml_data['class_profiles'][str(case)]['func_name']}_qosprotocol.pkl"
    with open(pkl, 'wb') as pkl_file:
        pickle.dump(eval(yml_data['class_profiles'][case]['func_name']), pkl_file, pickle.DEFAULT_PROTOCOL)

from network_topologies import *

TOPO_OUTDIR = f"{BASEDIR}/pkl/topo"
topo_yml = f"{BASEDIR}/config/topology_definitions.yml"

with open(topo_yml) as yml_file:
	yml_data = yaml.load(yml_file)

	for topo in yml_data['topology']:
		pkl = f"{TOPO_OUTDIR}/topo_{topo}.pkl"
		with open(pkl, 'wb') as pkl_file:
			pickle.dump(eval(topo), pkl_file, pickle.DEFAULT_PROTOCOL)







