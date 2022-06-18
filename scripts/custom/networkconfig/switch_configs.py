import csv
import yaml
import range_divider

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
            
        return f"name={name}\tdpid=00-00-00-00-00-0{dpid}\ttype={switch_type}\tcore_port={core_port}\tqueues={queues}\tqos={qos_type}\tqos_port={qos_port}\n"

    elif switch_type == 'client-leaf-ext':
        # print (f'client-leaf-ext test case: {test_case}')
        if test_case == 'leaves':
            queues = 3
            qos_port = core_port
        elif test_case == 'core':
            qos_type = 'none'
            qos_port = 0
        return f"name={name}\tdpid=00-00-00-00-00-0{dpid}\ttype={switch_type}\tleaf_ports={leaf_ports}\tcore_port={core_port}\tqueues={queues}\tqos={qos_type}\tqos_port={qos_port}\n"

    elif switch_type == 'core':
        first = int(name.split('switch')[1])-2
        second = int(name.split('switch')[1])-1
        leaf_ports = f'{first}:1,{second}:2'
        server_port = 3
        if test_case == 'leaves':
            queues = 0
            qos_port = 0
            qos_type = 'none'
        elif test_case == 'core':
            queues = 3
            qos_port = 3
            
        return f"name={name}\tdpid=00-00-00-00-00-0{dpid}\ttype={switch_type}\tleaf_ports={leaf_ports}\tserver_port={server_port}\tqueues={queues}\tqos={qos_type}\tqos_port={qos_port}\n"

    elif switch_type == 'server-leaf':
        qos_port = 0
        # core_port = 1
        return f"name={name}\tdpid=00-00-00-00-00-0{dpid}\ttype={switch_type}\tcore_port={core_port}\tqos={qos_type}\tqos_port={qos_port}\n"

def save_to_conf(basedir):

    # config_file = open(f"{basedir}/hosts.conf", "w")
    fat_tree = range_divider.switch_layers()
    print (fat_tree)
    yml = f"{basedir.split('custom')[0]}/simulate_topo.yml"
    usecase_yml = f"{basedir.split('custom')[0]}class_profile_functionname.yml"
    with open (yml, 'rb') as yml_file:
        topo = yaml.load(yml_file, Loader=yaml.FullLoader)

    with open(usecase_yml, 'rb') as yml_file:
        cases = yaml.load(yml_file, Loader=yaml.FullLoader)

    keys = len(fat_tree.keys())
    print (f"Keys: {keys}")
    print ("\n\n")

    for case in cases['class_profiles']:
        config_file = open(f"{basedir}/switches.case.{case}.conf", "w")
        qos_type = cases['class_profiles'][case]['qos_type']
        test_case = cases['class_profiles'][case]['test_case']
        layers = topo['topology']['fat_tree']['leaf_switch_layers']
        divider = range_divider.divider(topo['topology']['fat_tree']['clients'], 2 ** layers)
        layer_1 = fat_tree[1]
        core_switch = 'switch{}'.format(int(fat_tree[keys][1].split('h')[1])+1)
        server_switch = 'switch{}'.format(int(fat_tree[keys][1].split('h')[1])+2)
        start = 0

        for i in range(0, len(divider)):
            end = divider[i] - start
            start = divider[i]
            divider[i] = end

        for i in range(0, len(fat_tree[1])):
            qos_type = cases['class_profiles'][case]['qos_type']
            test_case = cases['class_profiles'][case]['test_case']
            core_port = divider[i] + 1
            name = fat_tree[1][i]
            dpid = name.split("switch")[1]
            config_file.write(generate_conf(name, dpid, 'client-leaf', core_port, None, qos_type, test_case))

        for i in range(2, keys+1):
            print (f'Layer {i} switches: {fat_tree[i]}')
            for j in range(0, len(fat_tree[i])):
                dpid = fat_tree[i][j].split("switch")[1]
                prev_layer = 2 ** layers
                print (f'switch: {fat_tree[i][j]}\tprev_layer: {prev_layer}')
                first =  (int(fat_tree[i][j].split('switch')[1]) - prev_layer) + j
                second = (int(fat_tree[i][j].split('switch')[1]) - prev_layer) + (j + 1)
                leaf_ports = f'{first}:1,{second}:2'
                config_file.write(generate_conf(fat_tree[i][j], dpid, 'client-leaf-ext', 3, leaf_ports, qos_type, test_case))
            print ('\n')
            layers = layers - 1

        first = int(core_switch.split('switch')[1])-2
        second = int(core_switch.split('switch')[1])-1
        leaf_ports = f'{first}:1,{second}:2'

        config_file.write(generate_conf(core_switch, core_switch.split("switch")[1], 'core', 3, leaf_ports, qos_type, test_case))
        config_file.write(generate_conf(server_switch, server_switch.split("switch")[1], 'server-leaf', 1, None, qos_type, test_case))

def main():
    save_to_conf()

if __name__ == '__main__':
    main()






















