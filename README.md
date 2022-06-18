# SDN-Framework-main

This is the documentation for the SDN QoS testing framework written by Josiah Elezar Regencia and William Emmanuel S. Yu.

# Configuration
Most configuration will be done in `config/class_profile_functionname.yml` and `config/topology_definitions.yml`

## Adding custom topology
First, place in the definition for your network topology in `scripts/network_topologies.py`
Then, add in the parameters needed for the network topology in `config/topology_definitions.yml`

## Custom Configuration and Scripts
The _Load Configuration_, _Source Queue Grouping Configuration_, _Hosts Configuration_ files are generated from the class profile and topology definitions file. More specifically, they are emitted by the calling `scripts/custom/network_configs.py` script.

`scripts/custom/network_configs.py` calls the following functions that need to be defined in the `scripts/custom/networkconfig` package:

- `clients`
- `load_conf`
- `source_queue`
- `switch_configs`
- `ovs_qosgenerator`
- `hosts`

`scripts/custom/node_connections.py` and `scripts/custom/nodes_config.py` is supposed to provide information about how the nodes are connected, however, they are not used in Regencia's tests.

# Using the test framework
First, generate the necessary pickle files and configuration files using `pkl_generator.sh`
Then, run `run_mininet.py` and `controller.py`