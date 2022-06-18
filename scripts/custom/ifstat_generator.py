import re
import os
import yaml
import range_divider

BASEDIR = os.getcwd()
ifstat = f"{BASEDIR}/measure/run-ipstat.sh"

filein = open(ifstat, 'rt')
cmd = filein.read()

fat_tree = range_divider.switch_layers()
keys = len(fat_tree.keys())
core_switch = 'switch{}-eth3'.format(int(fat_tree[keys][1].split('h')[1])+1)
init_intf = re.search("switch.*-eth.*", cmd)
changed_intf = init_intf.group().split(" ")[0]
cmd = cmd.replace(changed_intf, core_switch)
fileout = open(ifstat, 'wt')
fileout.write(cmd)
fileout.close()
os.system(f"chmod a+x {ifstat}")





