import csv
import yaml

###
# This module takes both the topology yml file and the class profile yml file.
# It emits the switches.case.(case number).conf file, which contains the following information:
# name: the name of the switch
# dpid: the unique identifier for a switch in mininet
# type: The type of the switch, for which there are the following kinds:
#   - client-leaf: the switches that connect directly to client hosts
#   - client-leaf-ext: the switches that are essentially internal nodes
#   - core: the root of the tree
#   - server-leaf: switches that are connected directly to server hosts
#  core_port: if not the root, the port with which the switch is connected to the parent
#  leaf_ports: if not the leaf, the ports with whcih the switch is connected to the children: format is {switch number}:{port number}
#  server_port: if the core, then the port where the server is connected to
#  qos: the qos algorithm being used, "none" if the switch does not enforce the qos
#  qos-port: the port which 
###

def dpid(switch_name):
    return int(switch_name.replace('switch', ''))

def generate_conf(name, dpid, switch_type, qos_type, test_case):
    queues = 0
    if switch_type == 'client-leaf':
        if test_case == 'leaves':
            queues = 3
        elif test_case == 'core':
            queues = 0
            qos_type = 'none'
        return f"name={name}\tdpid=00-00-00-00-00-{dpid:02}\ttype={switch_type}\tqueues={queues}\tqos={qos_type}\n"

    elif switch_type == 'client-leaf-ext':
        if test_case == 'leaves':
            queues = 3
        elif test_case == 'core':
            qos_type = 'none'
        return f"name={name}\tdpid=00-00-00-00-00-{dpid:02}\ttype={switch_type}\tqueues={queues}\tqos={qos_type}\n"

    elif switch_type == 'core':
        if test_case == 'leaves':
            queues = 0
            qos_type = 'none'
        elif test_case == 'core':
            queues = 3            
        return f"name={name}\tdpid=00-00-00-00-00-{dpid:02}\ttype={switch_type}\tqueues={queues}\tqos={qos_type}\n"

    elif switch_type == 'server-leaf':
        return f"name={name}\tdpid=00-00-00-00-00-{dpid:02}\ttype={switch_type}\tqos={qos_type}\n"

def save_to_conf(basedir, G):
    usecase_yml = f"{basedir.split('custom')[0]}class_profile_functionname.yml"

    with open(usecase_yml, 'rb') as yml_file:
        cases = yaml.load(yml_file, Loader=yaml.FullLoader)

    edge_switches = [node for node, data in G.nodes(data='type') if data=='edge_switch']
    internal_switches = [node for node, data in G.nodes(data='type') if data=='internal_switch']
    core_switch = G.graph['core_switch']
    server_switch = G.graph['server_switch']

    for case in cases['class_profiles']:
        config_file = open(f"{basedir}/switches.case.{case}.conf", "w")

        qos_type = cases['class_profiles'][case]['qos_type']
        test_case = cases['class_profiles'][case]['test_case']

        for edge_switch in edge_switches:
            dp_id = dpid(edge_switch)
            config_file.write(generate_conf(edge_switch, dp_id, 'client-leaf', qos_type, test_case))

        for internal_switch in internal_switches: # for now we assume that whatever switches have larger number are the leaves
            dp_id = dpid(internal_switch)
            config_file.write(generate_conf(internal_switch, dp_id, 'client-leaf-ext', qos_type, test_case))

        config_file.write(generate_conf(core_switch, dpid(core_switch), 'core', qos_type, test_case))
        config_file.write(generate_conf(server_switch, dpid(server_switch), 'server-leaf', qos_type, test_case))
        config_file.close()






















