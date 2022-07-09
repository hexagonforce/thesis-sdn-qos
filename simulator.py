from time import sleep
import yaml, csv
from run_mininet import create_network
from simulation import exec_ab_tests, exec_pings, setup_servers
from simulation import exec_ifstat, exec_vlc_client_probing, exec_vlc_clients
import subprocess
import os
from mininet.cli import CLI

BASEDIR = os.getcwd()
SERVERCONF = f'{BASEDIR}/config/server_config.yml'
LOADCONF = f'{BASEDIR}/config/custom/load.conf.l3.tab'
CONTROLLERCONF = f'{BASEDIR}/controller.conf'
CLASS_PROFILE_FILE = f'{BASEDIR}/config/class_profile_functionname.yml'
TOPO_FILE = f'{BASEDIR}/config/custom/topology_information.yml'
METADATA = f'{BASEDIR}/simulation/test.results/metadata.yml'

# Utility functions
def get_qos_type():
    return get_class_profile()['test_case']

def get_class_profile():
    class_profile_data = get_yml_data(CLASS_PROFILE_FILE)
    casenum = 0
    with open(CONTROLLERCONF, 'r') as file:
        for line in file:
            if line.startswith('case'):
                casenum = line.strip().split('=')[1].strip('"')
    class_profiles = class_profile_data['class_profiles']
    return class_profiles[casenum]

def get_yml_data(path):
    with open(path, 'r') as file:
        return yaml.load(file, Loader = yaml.FullLoader)

# Running functions
def writemetadata():
    '''
    This functions writes the Class Profile and the Topology used for the simulation run.
    '''
    metadata = {
        'func_name': get_class_profile(),
        'topology': get_yml_data(TOPO_FILE),
    }
    with open(METADATA, 'w') as file:
        yaml.dump(metadata, file)

def setup(serverdata):
    '''
    This function runs the scripts, starts mininet and Ryu, and configures the servers.
    '''
    subprocess.run(['sh', '-c', './runscripts.sh'])
    net = create_network()
    subprocess.run(['sh', '-c', './resetqos.sh'])
    subprocess.run(['sh', '-c', 'ryu-manager controller.py --config-file controller.conf > /dev/null 2> /dev/null &'])
    qostype = get_qos_type()
    subprocess.run(['sh', '-c', f'./setqos.sh > /dev/null {qostype}', ])
    setup_servers.setup_servers(net, serverdata)
    return net

def runtests(net, serverdata, loadconfig):
    '''
    This function runs all the tests of the research
    '''
    exec_pings.run(net)
    exec_ifstat.run()
    exec_ab_tests.run(net, serverdata, loadconfig)
    # exec_vlc_clients.run(net, serverdata, loadconfig)
    # exec_vlc_client_probing.run(net, serverdata, loadconfig)

# Entry point
if __name__ == '__main__':
    # Read all the necessary configuration files
    print("Started Simulation. Setting up the server...")
 
    serverdata = get_yml_data(SERVERCONF)

    net = setup(serverdata)
    loadconfdata = []
    with open(LOADCONF, 'r') as file:
        csvFile = csv.reader(file, delimiter='\t')
        for line in csvFile:
            loadconfdata.append(line)

    print("Setup Complete. Waiting for STP to converge...")
    sleep(30)
    print("Running tests. This may take a while...")
    writemetadata()
    runtests(net, serverdata, loadconfdata)
    CLI(net)
    net.stop()
    os.system("sudo pkill ryu-manager")


