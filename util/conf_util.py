import yaml
import csv
from util.constants import CONFIG_METADATA
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
    data = get_yml_data(CONFIG_METADATA)
    for k, v in data.items():
        if config in v:
            return f'config/custom/{v[config]}'
    return None
