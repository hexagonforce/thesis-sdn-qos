# Python packages
from time import sleep
from datetime import datetime
from sys import argv
import shutil
import yaml
import csv
import subprocess
from pathlib import Path
from os import environ

# Mininet library
from mininet.cli import CLI

# Custom code
import generate_configs
from run_mininet import create_network_networkx
from simulation import setup_servers, exec_ab_tests, exec_pings, exec_ifstat, exec_vlc_clients

BASEDIR = Path.cwd()
RUNCONF = BASEDIR / 'config/run_config.yml'
SERVERCONF = BASEDIR / 'config/server_config.yml'
LOADCONF = BASEDIR / 'config/custom/load.conf.l3.tab'
CONTROLLERCONF = BASEDIR / 'controller.conf'
CLASS_PROFILE_FILE = BASEDIR / 'config/class_profile_functionname.yml'
SIMULATION_RESULTS = BASEDIR / 'simulation/test.results'
SIMULATION_LOGS = BASEDIR / 'simulation/server-logs'
RESULTS_ARCHIVE_DIRECTORY = Path(f"/home/{environ.get('SUDO_USER', 'mininet')}/results")

# Utility functions
def get_yml_data(path):
    with open(path, 'r') as file:
        return yaml.load(file, Loader = yaml.FullLoader)

def get_class_profile_num():
    '''
    This reads from controller.conf
    '''
    casenum = 0
    with open(CONTROLLERCONF, 'r') as file:
        for line in file:
            if line.startswith('case'):
                casenum = line.strip().split('=')[1].strip('"')
                break
    return casenum

def get_class_profile():
    casenum = get_class_profile_num()
    class_profile_data = get_yml_data(CLASS_PROFILE_FILE)
    class_profiles = class_profile_data['class_profiles']
    return class_profiles[casenum]

def get_qos_type():
    return get_class_profile()['test_case']

def export_results(result_file_name):
    if not RESULTS_ARCHIVE_DIRECTORY.exists():
        RESULTS_ARCHIVE_DIRECTORY.mkdir()
    shutil.make_archive(
        str(RESULTS_ARCHIVE_DIRECTORY / result_file_name), 'zip', 
        root_dir=SIMULATION_RESULTS, base_dir='.'
    )

def main(iterations=1):
    run_start_time = datetime.now().replace(microsecond=0)
    print("Preparing the necessary configuration files...")

    # Read the main configuration file
    runconf = get_yml_data(RUNCONF)
    topology = runconf['topology']
    case = runconf['case']

    # Read server_config and load.conf.l3.tab
    serverdata = get_yml_data(SERVERCONF)
    loadconfdata = []
    with open(LOADCONF, 'r') as file:
        csvFile = csv.reader(file, delimiter='\t')
        for line in csvFile:
            loadconfdata.append(line)

    # Generate topology and configuration files
    G = generate_configs.generate_graph(topology)
    generate_configs.configure(G, case)

    # Set up the network
    net = create_network_networkx(G)
    core_switch = G.graph['core_switch']

    # Sends the information about the core switch of the topology to the Ryu Controller configuration file
    with open(CONTROLLERCONF, 'w') as controller_config:
        controller_config.write(
            f'[DEFAULT]\ncase="{case}"\ncore_switch="{core_switch}'
        )

    # Setup OpenFlow queue settings
    subprocess.run(['sudo', 'ovs-vsctl', '--all', 'destroy', 'qos'])
    subprocess.run(['sudo', 'ovs-vsctl', '--all', 'destroy', 'queue'])
    subprocess.run([f'./config/custom/run.ovs-vsctl.case.{get_qos_type()}.sh'], stdout=subprocess.DEVNULL)

    print("Done preparing the configuration files.")



    # Execute test suite
    try:
        print("Setting up the controller and the servers.")
        # Runs the controller
        ryu_manager = subprocess.Popen(['ryu-manager', 'controller.py', '--config-file', 'controller.conf'], stderr=open('ryu_error.txt', 'w'))
        # Set up servers in the network
        server_processes = setup_servers.run(net, serverdata)

        # Wait for STP
        print("Setup Complete. Waiting for STP...")
        sleep(60)
        print("Now running tests. This may take a while...")

        # Test pings once, because it's not necessary to test them all the time
        exec_pings.run_all_pings(net)

        for idx in range(int(iterations)):
            # Reset the results directory
            subprocess.run(['rm', '-rf', 'simulation/test.results/'])
            subprocess.run(['sudo', '-u' 'mininet', 'mkdir', 'simulation/test.results'])
            subprocess.run(['sudo', '-u', 'mininet', 'mkdir', 'metadata', 'ab-tests', 'pings', 'vlc-clients'], cwd=f'{BASEDIR}/simulation/test.results')
            subprocess.run(['sh', '-c', f'cp {BASEDIR}/config/*ml {SIMULATION_RESULTS}/metadata']) # All files ending in ml are metadata
            start_time = datetime.now().replace(microsecond=0)
            
            print(f'Executing test {idx+1}/{iterations}...')
            # Execute pings
            exec_pings.test_convergence(net)

            # Execute the rest of the tests
            exec_ifstat.run(G)
            vlc_processes = exec_vlc_clients.run(net, serverdata, loadconfdata)
            hey_processes = exec_ab_tests.run(net, serverdata, loadconfdata)
            
    
            # Stop only when all the processes have exited correctly 
            while True:
                running = False
                for process in vlc_processes + hey_processes:
                    if process.poll() is None:
                        running = True
                        break
                if not running:
                    sleep(5)
                    break
                sleep(5)
            filename = f'{start_time.isoformat()}-{get_class_profile_num()}-{get_qos_type()}-{G.graph["name"]}'
            print(f"Done with test {idx+1}. Now saving test results.")
            export_results(filename)
    except Exception as e:
        print("There was an error. The error message is as follows:")
        print(e)
    finally:
        net.stop()
        ryu_manager.terminate()
        for process in server_processes:
            process.terminate()
        shutil.make_archive(
            str(RESULTS_ARCHIVE_DIRECTORY / f'{run_start_time.isoformat()}-logs'), 'zip', 
            root_dir=SIMULATION_LOGS, base_dir='.'
        )

if __name__ == '__main__':
    main(*argv[1:])
