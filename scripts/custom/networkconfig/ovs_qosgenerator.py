# Outputs to scripts/custom/run.ovs-vsctl.case a script that sets QoS constraints with the ovs-vsctl utility
# Modify the generate_script method to change the actual QoS constraints
#

import os
import yaml
import range_divider

def generate_script(interface):
    return f"sudo ovs-vsctl -- set Port {interface} qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2\n"

def save_to_conf(basedir, execdir):
    print (f"BASEDIR: {basedir}")
    yml = f"{basedir.split('custom')[0]}/simulate_topo.yml"
    usecase_yml = f"{basedir.split('custom')[0]}/classprofile_functionname.yml"
    cases = ["at_core", "at_leaf"]
    with open (yml, 'rb') as yml_file:
        topo = yaml.load(yml_file, Loader=yaml.FullLoader)

    layers = topo['topology']['fat_tree']['leaf_switch_layers']
    clients = topo['topology']['fat_tree']['clients']
    fat_tree = range_divider.switch_layers()
    ranges = range_divider.divider(clients, 2 ** layers)
    keys = len(fat_tree.keys())
    core_switch = f"switch{int(fat_tree[keys][1].split('h')[1])+1}"
    print (f"Switch Layers: {fat_tree}")
    print (f"\nDivider: {ranges}\n\n")
    outports = [ranges[0]+1]
    for i in range(1, len(ranges)):
        outports.append((ranges[i]-ranges[i-1])+1)
    print (f"Outports : {outports}")

    for case in cases:
        config_file = open(f"{execdir}/run.ovs-vsctl.case.{case}.sh", "w")
        if case == "at_core":
            print (f"\n{case}")
            interface = f"{core_switch}-eth3"
            config_file.write(generate_script(interface))

        elif case == "at_leaf":
            print (f"\n{case}")
            for i in range(0, len(fat_tree[1])):
                interface = f"{fat_tree[1][i]}-eth{outports[i]}"
                config_file.write(generate_script(interface))

            for i in range(2, keys+1):
                for switch in fat_tree[i]:
                    interface = f"{switch}-eth3"
                    config_file.write(generate_script(interface))







