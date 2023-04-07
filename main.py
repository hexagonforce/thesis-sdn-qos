'''
This is the main file of the testing framework.
Usage: sudo python3 main.py [args].

Arguments:
    iterations: Number of times the script will run the HTTP and Video streaming tests
'''

# Python packages
from time import sleep
from datetime import datetime
from sys import argv
from shutil import make_archive, rmtree
import subprocess
from pathlib import Path
import networkx as nx

# Mininet library
from mininet.cli import CLI

# Custom code
from scripts import network_topologies
from scripts.custom import network_configs, nodes_config
from run_mininet import start_mininet_from_networkx_graph
from simulation import setup_servers, exec_ab_tests, exec_pings, exec_ifstat, exec_vlc_clients
from util.conf_util import get_csv_data, get_yml_data
from util.constants import *

def get_qos_type(casenum):
    class_profile_data = get_yml_data(CLASS_PROFILE_FILE)
    class_profiles = class_profile_data['class_profiles']
    return class_profiles[casenum]['test_case']

def export_results(result_file_name):
    if not RESULTS_ARCHIVE_DIRECTORY.exists():
        RESULTS_ARCHIVE_DIRECTORY.mkdir()
    make_archive(
        str(RESULTS_ARCHIVE_DIRECTORY / result_file_name), 'zip', 
        root_dir=SIMULATION_RESULTS, base_dir='.'
    )

def reset_test_results_directory():
    rmtree('simulation/test.results/')
    subprocess.run(['sudo', '-u' 'mininet', 'mkdir', 'simulation/test.results'])
    Path.mkdir('simulation/test.results')
    for folder_name in ['metadata', 'ab-tests', 'pings', 'vlc-clients']:
        Path.mkdir(f'simulation/test.results/{folder_name}')
    subprocess.run(['sh', '-c', f'cp {BASEDIR}/config/*ml {SIMULATION_RESULTS}/metadata'])

def main(iterations=1):
    print("Preparing the necessary configuration files...")
    run_start_time = datetime.now().replace(microsecond=0)
    reset_test_results_directory()

    # Read the main configuration file
    runconf = get_yml_data(RUNCONF)
    topology = runconf['topology']
    casenum = runconf['case']
    qos_type = get_qos_type(casenum)

    # Read server_config and load.conf.l3.tab
    serverdata = get_yml_data(SERVERCONF)
    loadconfdata = get_csv_data(LOADCONF)

    # Generate topology and configuration files
    G = network_topologies.get_topology_graph(topology)
    network_configs.generate_all_configs(G) # intention is to pass networkx graph to everyone
    nodes_config.write_all_config_to_json(casenum)
    nx.write_graphml(G, f'{BASEDIR}/config/topology.graphml')

    # Set up the network
    net = start_mininet_from_networkx_graph(G)
    core_switch = G.graph['core_switch']

    # Sends the information about the core switch of the topology to the Ryu Controller configuration file
    with open(CONTROLLERCONF, 'w') as controller_config:
        controller_config.write(
            f'[DEFAULT]\ncase="{casenum}"\ncore_switch="{core_switch}'
        )

    # Setup OpenFlow queue settings
    subprocess.run(['sudo', 'ovs-vsctl', '--all', 'destroy', 'qos'])
    subprocess.run(['sudo', 'ovs-vsctl', '--all', 'destroy', 'queue'])
    subprocess.run([f'./config/custom/run.ovs-vsctl.case.{qos_type}.sh'], stdout=subprocess.DEVNULL)

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
        exec_pings.test_convergence(net)
        exec_pings.run_all_pings(net)

        for idx in range(int(iterations)):
            # Reset the results directory
            start_time = datetime.now().replace(microsecond=0)
            
            print(f'Executing test {idx+1}/{iterations}...')

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
            # Save the run and reset the test results directory
            print(f"Done with test {idx+1}. Now saving test results.")

            filename = f'{start_time.isoformat()}-{casenum}-{qos_type}-{G.graph["name"]}'
            export_results(filename)
            reset_test_results_directory()

    except Exception as e:
        print("There was an error. The error message is as follows:")
        print(e)
    finally:
        net.stop()
        ryu_manager.terminate()
        for process in server_processes:
            process.terminate()
        make_archive(
            str(RESULTS_ARCHIVE_DIRECTORY / f'{run_start_time.isoformat()}-logs'), 'zip', 
            root_dir=SIMULATION_LOGS, base_dir='.'
        )

if __name__ == '__main__':
    main(*argv[1:])
