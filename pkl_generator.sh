#!/bin/bash

# python3 scripts/custom/network_configs.py
# python3 scripts/custom/nodes_config.py
# python3 scripts/custom/node_connections.py
# python3 scripts/custom/ifstat_generator.py

python3 scripts/serialize.py
for file in scripts/custom/*.py; do python3 "$file"; done

sudo pkill -f python3
sudo pkill -f vlc