import os, yaml, subprocess

BASEDIR = os.getcwd()

def run(G):
    core_switch = G.graph['core_switch']
    server_switch = G.graph['server_switch']

    if core_switch < server_switch:
        core_switch_port = G[core_switch][server_switch]['lport']
    else:
        core_switch_port = G[server_switch][core_switch]['rport']


    core_switch = f'{core_switch}-eth{core_switch_port}'
    csvfile = f'{BASEDIR}/simulation/test.results/ifstat-results.csv'
    with open(csvfile, 'w') as file:
        subprocess.Popen(['timeout', '600s', 'sudo', '-u', 'mininet', 'ifstat', '-i', core_switch,
                        '-t', '-n'], stdout=file)
