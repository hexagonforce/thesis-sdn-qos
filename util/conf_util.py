import yaml
import csv

def get_yml_data(path):
    with open(path, 'r') as file:
        return yaml.load(file, Loader = yaml.FullLoader)
    
def get_csv_data(path, delimiter='\t'):
    ret = []
    with open(path, 'r') as file:
        csvFile = csv.reader(file, delimiter=delimiter)
        for line in csvFile:
            ret.append(line)
    return ret

def get_path_of_gen_config(config):
    data = get_yml_data(config)
    for k, v in data.items():
        if config in v:
            return f'config/custom/{v[config]}'
    return None