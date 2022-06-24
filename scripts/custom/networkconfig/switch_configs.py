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
#   - core_port: if not the root, the port with which the switch is connected to the parent
#   - leaf_ports: if not the leaf, the ports with whcih the switch is connected to the children: format is {switch number}:{port number}
#   - server_port: if the core, then the port where the server is connected to
#   - qos: the qos algorithm being used, "none" if the switch does not enforce the qos
#   - qos-port: the port which 
###

def dpid(switch_name):
    return int(switch_name.replace('switch', ''))

def generate_conf(name, dpid, switch_type, core_port, leaf_ports, qos_type, test_case):
    queues = 0
    if switch_type == 'client-leaf':
        if test_case == 'leaves':
            queues = 3
            qos_port = core_port
        elif test_case == 'core':
            queues = 0
            qos_port = 0
            qos_type = 'none'
            
        return f"name={name}\tdpid=00-00-00-00-00-{dpid:02}\ttype={switch_type}\tcore_port={core_port}\tqueues={queues}\tqos={qos_type}\tqos_port={qos_port}\n"

    elif switch_type == 'client-leaf-ext':
        # print (f'client-leaf-ext test case: {test_case}')
        if test_case == 'leaves':
            queues = 3
            qos_port = core_port
        elif test_case == 'core':
            qos_type = 'none'
            qos_port = 0
        return f"name={name}\tdpid=00-00-00-00-00-{dpid:02}\ttype={switch_type}\tleaf_ports={leaf_ports}\tcore_port={core_port}\tqueues={queues}\tqos={qos_type}\tqos_port={qos_port}\n"

    elif switch_type == 'core':
        server_port = core_port
        if test_case == 'leaves':
            queues = 0
            qos_port = 0
            qos_type = 'none'
        elif test_case == 'core':
            queues = 3
            qos_port = server_port
            
        return f"name={name}\tdpid=00-00-00-00-00-{dpid:02}\ttype={switch_type}\tleaf_ports={leaf_ports}\tserver_port={server_port}\tqueues={queues}\tqos={qos_type}\tqos_port={qos_port}\n"

    elif switch_type == 'server-leaf':
        qos_port = 0
        # core_port = 1
        return f"name={name}\tdpid=00-00-00-00-00-{dpid:02}\ttype={switch_type}\tcore_port={core_port}\tqos={qos_type}\tqos_port={qos_port}\n"

def save_to_conf(basedir):
    usecase_yml = f"{basedir.split('custom')[0]}class_profile_functionname.yml"
    topo_yml = f"{basedir}/topology_information.yml"

    with open (topo_yml, 'rb') as yml_file:
        topo = yaml.load(yml_file, Loader=yaml.FullLoader)

    with open(usecase_yml, 'rb') as yml_file:
        cases = yaml.load(yml_file, Loader=yaml.FullLoader)

    for case in cases['class_profiles']:
        config_file = open(f"{basedir}/switches.case.{case}.conf", "w")

        qos_type = cases['class_profiles'][case]['qos_type']
        test_case = cases['class_profiles'][case]['test_case']
        core_switch = topo['core_switch']
        server_switch = topo['server_switch']
        edge_switches = topo['edge_switches']

        for edge_switch in edge_switches:
            core_port = sum(1 for node in topo['adjlist'][edge_switch] if 'client' in node) + 1
            dp_id = dpid(edge_switch)
            config_file.write(generate_conf(edge_switch, dp_id, 'client-leaf', core_port, None, qos_type, test_case))

        for internal_switch in topo['internal_switches']: # for now we assume that whatever switches have larger number are the leaves
            dp_id = dpid(internal_switch)
            leaf_ports=','.join((f"{dpid(node)}:{portnum}" for (node, portnum) 
                        in topo['adjlist'][internal_switch].items()
                        if 'switch' in node and dpid(node) > dp_id))
            core_port = sum(1 for node in topo['adjlist'][edge_switch] if 'client' in node)
            config_file.write(generate_conf(internal_switch, dp_id, 'client-leaf-ext', 1, leaf_ports, qos_type, test_case))


        leaf_of_core = ','.join((f"{dpid(node)}:{portnum}" for (node, portnum) 
                        in topo['adjlist'][core_switch].items()
                        if 'switch' in node and 
                        dpid(node) > dpid(core_switch) and 
                        dpid(node) != dpid(server_switch)))
        # due to the idiosyncracies of current code, core port of the core switch is defined
        # to be the port that connects the core switch to the server switch
        core_port = topo['adjlist'][core_switch][server_switch]
        server_to_core = topo['adjlist'][core_switch][server_switch]
        config_file.write(generate_conf(core_switch, dpid(core_switch), 'core', core_port, leaf_of_core, qos_type, test_case))
        config_file.write(generate_conf(server_switch, dpid(server_switch), 'server-leaf', server_to_core, None, qos_type, test_case))
        config_file.close()

def main():
    save_to_conf()

if __name__ == '__main__':
    main()






















