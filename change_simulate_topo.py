from sys import argv
from yaml import safe_load, dump

def main(argv):
    with open('config/simulate_topo.yml', 'r') as simulate_topo_file:
       simulate_topo_dict = safe_load(simulate_topo_file)
    with open('config/run_config.yml', 'r') as run_config_file:
        run_config_dict = safe_load(run_config_file)

    change_type = argv[0]
    value = argv[1]
    if (change_type == 'ITZ'):
        simulate_topo_dict['zoo']['details']['filename'] = f'{value}.graphml'
        run_config_dict['topology'] = 'zoo'
    else:
        run_config_dict['topology'] = value

    with open('config/run_config.yml', 'w') as run_config_file:
        dump(run_config_dict, run_config_file)

    with open('config/simulate_topo.yml', 'w') as simulate_topo_file:
        dump(simulate_topo_dict, simulate_topo_file)

if __name__ == '__main__':
    main(argv[1:])
