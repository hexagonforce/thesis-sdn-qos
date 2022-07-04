# Outputs to scripts/custom/run.ovs-vsctl.case a script that sets QoS constraints with the ovs-vsctl utility
# Modify the generate_script method to change the actual QoS constraints
#

import os
import yaml

def generate_script(interface):
    return f"sudo ovs-vsctl -- set Port {interface} qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2\n"

def save_to_conf(basedir, execdir):
    # print (f"BASEDIR: {basedir}")
    yml = f"{basedir}/topology_information.yml"
    usecase_yml = f"{basedir.split('custom')[0]}/classprofile_functionname.yml"
    cases = ["at_core", "at_leaf"]
    with open (yml, 'rb') as yml_file:
        topo = yaml.load(yml_file, Loader=yaml.FullLoader)

    core_switch = topo['core_switch']
    server_switch = topo['server_switch']


    for case in cases:
        config_file = open(f"{execdir}/run.ovs-vsctl.case.{case}.sh", "w")
        if case == "at_core":
            to_server_port = ''
            to_core_port = ''
            for node, port in topo['adjlist'][core_switch].items():
                if node == server_switch:
                    to_server_port = port
                    break
            for node, port in topo['adjlist'][server_switch].items():
                if node == core_switch:
                    to_core_port = port
                    break
            interface = f"{core_switch}-eth{to_server_port}"
            config_file.write(generate_script(interface))
            interface2 = f"{server_switch}-eth{to_core_port}"
            config_file.write(generate_script(interface2))

        elif case == "at_leaf":
            for switch in topo['edge_switches'] + topo['internal_switches']:
                for node, port in topo['adjlist'][switch].items():
                    config_file.write(generate_script(f"{switch}-eth{port}"))
        os.system(f"chmod a+x {execdir}/run.ovs-vsctl.case.{case}.sh")
        








