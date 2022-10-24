# Outputs to scripts/custom/run.ovs-vsctl.case a script that sets QoS constraints with the ovs-vsctl utility
# Modify the generate_script method to change the actual QoS constraints
#

import yaml, subprocess

def generate_script(interface):
    return f"sudo ovs-vsctl -- set Port {interface} qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2\n"
        
def save_to_conf(execdir, G):
    cases = ["core", "leaves"]
    core_switch = G.graph['core_switch']
    server_switch = G.graph['server_switch']
    edge_switches = [node for node, data in G.nodes(data='type') if data=='edge_switch']
    internal_switches = [node for node, data in G.nodes(data='type') if data=='internal_switch']

    for case in cases:
        config_file = open(f"{execdir}/run.ovs-vsctl.case.{case}.sh", "w")
        config_file.write("#! /usr/bin/bash\n")
        if case == "core":
            to_server = G[core_switch][server_switch]['lport']
            to_core = G[core_switch][server_switch]['rport']
            config_file.write(generate_script(f"{core_switch}-eth{to_server}"))
            config_file.write(generate_script(f"{server_switch}-eth{to_core}"))

        elif case == "leaves":
            for switch in edge_switches + internal_switches:
                for neighbor in G[switch]:
                    if (switch < neighbor):
                        port = G[switch][neighbor]['lport']
                    else:
                        port = G[switch][neighbor]['rport']
                    config_file.write(generate_script(f"{switch}-eth{port}"))
        config_file.close()
        subprocess.run(['chmod', 'u+x', f'{execdir}/run.ovs-vsctl.case.{case}.sh'])
