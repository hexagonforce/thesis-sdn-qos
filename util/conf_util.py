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