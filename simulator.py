from time import sleep
import psutil
import yaml, csv
import subprocess
import os
from mininet.cli import CLI

import generate_configs
from run_mininet import create_network_networkx
from simulation import setup_servers, exec_ab_tests, exec_pings, exec_ifstat, exec_vlc_clients

BASEDIR = os.getcwd()
SERVERCONF = f'{BASEDIR}/config/server_config.yml'
LOADCONF = f'{BASEDIR}/config/custom/load.conf.l3.tab'
CONTROLLERCONF = f'{BASEDIR}/controller.conf'
CLASS_PROFILE_FILE = f'{BASEDIR}/config/class_profile_functionname.yml'
METADATA = f'{BASEDIR}/simulation/test.results/metadata/'

# Utility functions
def get_qos_type():
    return get_class_profile()['test_case']

def get_class_profile():
    '''
    This reads from the class profile yaml file and gets the corresponding 
    '''
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

def main():
    print("Started Simulation. Setting up the server...")

    # Reset the results directory
    subprocess.run(['rm', '-rf', 'simulation/test.results/'])
    subprocess.run(['sudo', '-u' 'mininet', 'mkdir', 'simulation/test.results'])
    subprocess.run(['sudo', '-u', 'mininet', 'mkdir', 'metadata', 'ab-tests', 'pings', 'vlc-clients', 'vlc-server'], cwd=f'{BASEDIR}/simulation/test.results')
    subprocess.run(['sh', '-c', f'cp {BASEDIR}/config/*.yml {METADATA}'])

    # Generate topology and configuration files
    G = generate_configs.generate_graph()
    generate_configs.configure(G)

    # Read server_config and load.conf.l3.tab
    serverdata = get_yml_data(SERVERCONF)
    loadconfdata = []
    with open(LOADCONF, 'r') as file:
        csvFile = csv.reader(file, delimiter='\t')
        for line in csvFile:
            loadconfdata.append(line)
    
    # Set up the network
    net = create_network_networkx(G)
    core_switch = G.graph['core_switch']

    # Sends the information about the core switch of the topology to the Ryu Controller configuration file
    with open(CONTROLLERCONF, 'r+') as controller_config:
        lines = controller_config.readlines()
    with open(CONTROLLERCONF, 'w') as controller_config:
        for line in lines:
            if line.startswith('core_switch'):
                controller_config.write(f'core_switch="{core_switch}"\n')
            else:
                controller_config.write(line)

    # Setup OpenFlow queue settings
    subprocess.run(['sudo', 'ovs-vsctl', '--all', 'destroy', 'qos'])
    subprocess.run(['sudo', 'ovs-vsctl', '--all', 'destroy', 'queue'])
    subprocess.run([f'./config/custom/run.ovs-vsctl.case.{get_qos_type()}.sh'], stdout=subprocess.DEVNULL)

    # Runs the controller
    subprocess.Popen(['ryu-manager', 'controller.py', '--config-file', 'controller.conf'], stderr=open('ryuerr.txt', 'w'))

    # Set up servers in the network
    setup_servers.run(net, serverdata)

    # Wait for STP
    print("Setup Complete. Waiting for STP...")
    sleep(60)
    print("Running tests. This may take a while...")

    # Execute pings
    # exec_pings.test_convergence(net)
    # exec_pings.run_all_pings(net)

    # Execute test suite
    exec_ifstat.run(G)
    exec_vlc_clients.run(net, serverdata, loadconfdata)
    exec_ab_tests.run(net, serverdata, loadconfdata)

    # Control the length of simulation
    while True:
        sleep(5)
        processes = [x.name() for x in psutil.process_iter()]
        if processes.count('hey') == 0:
            sleep(30)
            break

    # Stop everything
    # CLI(net)
    net.stop()
    subprocess.run(["sudo", "pkill", "ryu-manager"])
    subprocess.run(["sudo", "pkill", "vlc"])
    subprocess.run(["sudo", "pkill", "cvlc"])
    subprocess.run(["sudo", "pkill", "ifstat"])


# Entry point
if __name__ == '__main__':
    main()
