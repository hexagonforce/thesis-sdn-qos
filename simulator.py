from time import sleep
import yaml, csv
from run_mininet import create_network
from simulation import setup_servers, exec_ab_tests, exec_pings, exec_ifstat, exec_vlc_clients
import subprocess
import os
from mininet.cli import CLI

BASEDIR = os.getcwd()
SERVERCONF = f'{BASEDIR}/config/server_config.yml'
LOADCONF = f'{BASEDIR}/config/custom/load.conf.l3.tab'
CONTROLLERCONF = f'{BASEDIR}/controller.conf'
CLASS_PROFILE_FILE = f'{BASEDIR}/config/class_profile_functionname.yml'
TOPO_FILE = f'{BASEDIR}/config/custom/topology_information.yml'
METADATA = f'{BASEDIR}/simulation/test.results/metadata/'

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
def setup_directories():
    '''
    This function copies over config files to the results directory
    '''
    subprocess.run(['rm', '-rf', 'simulation/test.results/'])
    subprocess.run(['sudo', '-u' 'mininet', 'mkdir', 'simulation/test.results'])
    subprocess.run(['sudo', '-u', 'mininet', 'mkdir', 'metadata', 'ab-tests', 'queue-stats', 'pings', 'vlc-clients', 'vlc-server'], cwd=f'{BASEDIR}/simulation/test.results')
    subprocess.run(['sh', '-c', f'cp {BASEDIR}/config/*.yml {METADATA}'])
    subprocess.run(['sh', '-c', f'cp {BASEDIR}/config/custom/topology_information.yml {METADATA}'])

def setup(serverdata):
    '''
    This function runs the scripts, starts mininet and Ryu, and configures the servers.
    '''
    subprocess.run(['./runscripts.sh'])
    net = create_network()
    subprocess.run(['sudo', 'ovs-vsctl', '--all', 'destroy', 'qos'])
    subprocess.run(['sudo', 'ovs-vsctl', '--all', 'destroy', 'queue'])
    subprocess.run(['sh', '-c', 'ryu-manager controller.py --config-file controller.conf > /dev/null 2> /dev/null &'])
    subprocess.run(['sh', '-c', f'./setqos.sh {get_qos_type()} > /dev/null', ])
    setup_servers.run(net, serverdata)
    return net

def runtests(net, serverdata, loadconfig):
    '''
    This function runs all the tests of the research
    '''
    exec_pings.run(net)
    print("Done with pings. Now running traffic tests...")
    exec_ifstat.run()
    exec_ab_tests.run(net, serverdata, loadconfig)
    exec_vlc_clients.run(net, serverdata, loadconfig)

# Entry point
if __name__ == '__main__':
    # Read all the necessary configuration files
    print("Started Simulation. Setting up the server...")
 
    setup_directories()
    serverdata = get_yml_data(SERVERCONF)
    net = setup(serverdata)
    loadconfdata = []
    with open(LOADCONF, 'r') as file:
        csvFile = csv.reader(file, delimiter='\t')
        for line in csvFile:
            loadconfdata.append(line)

    print("Setup Complete. Waiting for STP...")
    sleep(40)
    print("Running tests. This may take a while...")
    runtests(net, serverdata, loadconfdata)
    CLI(net)
    net.stop()
    subprocess.run(["sudo", "pkill", "ryu-manager"])
    subprocess.run(["sudo", "pkill", "vlc"])
    subprocess.run(["sudo", "pkill", "cvlc"])



