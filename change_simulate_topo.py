from sys import argv
from yaml import safe_load, dump
def main(argv):
    with open('config/simulate_topo.yml', 'r') as simulate_topo_file:
       simulate_topo_map = safe_load(simulate_topo_file)
    change_type = argv[0]
    value = argv[1]
    if (change_type == 'ITZ'):
        simulate_topo_map['to_test'] = 'Zoo'
        simulate_topo_map['topology']['Zoo']['details']['filename'] = f'{value}.graphml'
    else:
        simulate_topo_map['to_test'] = value
    with open('config/simulate_topo.yml', 'w') as simulate_topo_file:
        yee = dump(simulate_topo_map, simulate_topo_file)
if __name__ == '__main__':
    main(argv[1:])
