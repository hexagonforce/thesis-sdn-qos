import os, yaml, subprocess

BASEDIR = os.getcwd()
TOPO_INFO = f'{BASEDIR}/config/custom/topology_information.yml'

def run():
    with open(TOPO_INFO, 'r') as yml_data:
        topo_data = yaml.load(yml_data, Loader=yaml.FullLoader)

    core_switch = topo_data['core_switch']
    server_switch = topo_data['server_switch']

    core_switch_port = 0
    for dest, port in topo_data['adjlist'][core_switch].items():
        if (dest == server_switch):
            core_switch_port = port
            break

    core_switch = f'{core_switch}-eth{core_switch_port}'
    cmd = (
        f'timeout 330s sudo -u mininet ifstat -i {core_switch}'
        f' -t -n > {BASEDIR}/simulation/test.results/ifstat-results.csv &'
    )
    csvfile = f'{BASEDIR}/simulation/test.results/ifstat-results.csv'
    with open(csvfile, 'w') as file:
        subprocess.Popen(['timeout', '330s', 'sudo', '-u', 'mininet', 'ifstat', '-i', core_switch,
                        '-t', '-n'], stdout=file)
