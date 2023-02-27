# Outputs to scripts/custom/run.ovs-vsctl.case a script that sets QoS constraints with the ovs-vsctl utility
# Modify the generate_script method to change the actual QoS constraints
#

import yaml, subprocess
from pathlib import Path

def generate_script(interface, priorities):
    return (
        f"sudo ovs-vsctl -- set Port {interface} qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- "
        f"--id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority={priorities[0]} -- "
        f"--id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority={priorities[1]} -- "
        f"--id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority={priorities[2]}\n"
    )


def get_qos_type():
    config_path = Path.cwd() / 'config'
    with open(config_path / 'run_config.yml') as file:
        temp = yaml.safe_load(file)
        casenum = temp['case']
    with open(config_path / 'class_profile_functionname.yml') as file:
        temp = yaml.safe_load(file)
        return temp['class_profiles'][casenum]['qos_type']

def save_to_conf(execdir, G):
    cases = ["core", "leaves"]
    core_switch = G.graph['core_switch']
    server_switch = G.graph['server_switch']
    edge_switches = [node for node, data in G.nodes(data='type') if data=='edge_switch']
    internal_switches = [node for node, data in G.nodes(data='type') if data=='internal_switch']

    priorities_dict = {
        'basic': (1, 2, 0),
        'source': (1, 1, 1),
    }

    priorities = priorities_dict[get_qos_type()]

    for case in cases:
        config_file = open(f"{execdir}/run.ovs-vsctl.case.{case}.sh", "w")
        config_file.write("#! /usr/bin/bash\n")
        if case == "core":
            to_server = G[core_switch][server_switch]['lport']
            to_core = G[core_switch][server_switch]['rport']
            config_file.write(generate_script(f"{core_switch}-eth{to_server}", priorities))
            config_file.write(generate_script(f"{server_switch}-eth{to_core}", priorities))

        elif case == "leaves":
            for switch in edge_switches + internal_switches:
                for neighbor in G[switch]:
                    if (switch < neighbor):
                        port = G[switch][neighbor]['lport']
                    else:
                        port = G[switch][neighbor]['rport']
                    config_file.write(generate_script(f"{switch}-eth{port}", priorities))
        config_file.close()
        subprocess.run(['chmod', 'u+x', f'{execdir}/run.ovs-vsctl.case.{case}.sh'])
