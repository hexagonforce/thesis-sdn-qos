# SDN-Framework-main

This is the documentation for the SDN QoS testing framework written by Josiah Elezar Regencia and William Emmanuel S. Yu.

# Configuration
Most configuration will be done in `config/class_profile_functionname.yml` and `config/simulate_topo.yml`

## Adding custom topology
First, place in the definition for your network topology in `scripts/network_topologies.py`
Then, add in the parameters needed for the network topology in `config/simulate_topo.yml`
If you want to use your own GraphML file, the place it in the `zoo_data` directory and 

## Custom Configuration and Scripts
The _Load Configuration_, _Source Queue Grouping Configuration_, _Hosts Configuration_ files are generated from the class profile and topology definitions file. More specifically, they are emitted by the calling `scripts/custom/network_configs.py` script.

`scripts/custom/network_configs.py` calls the following functions that need to be defined in the `scripts/custom/networkconfig` package:

- `clients`
- `load_conf`
- `source_queue`
- `switch_configs`
- `ovs_qosgenerator`
- `hosts`

`scripts/custom/node_connections.py` and `scripts/custom/nodes_config.py` is supposed to provide information about how the nodes are connected, however, I have no idea what they do.

# Using the test framework
Remember to change the directories for `measure/run-ipstat.sh`.

First, generate the necessary pickle files and configuration files using `runscripts.sh`
<!--Then, run the pcap/oneway_preprocess.py to generate the correct vhost_mapping-->

Then, run `run_mininet.py` to start the Mininet topology.
Then, run `reset_qos.sh at_leaf` to reset the OVS Switch QoS settings.
Then start the Ryu controller using `Controller.sh`.

Alternatively, run `simulator.py` to run all the scripts and tests automatically.

# Replicating previous research with apachebenchmark and VLC
- Start the Python3 http webservers by running appropriate bash commands
- Start the VLC VOD servers by running appropriate bash commands
- Start the ifstat command with `measure/run-ipstat.sh
- Make the requests. For each client, make 1 HTTP request and 1 VLC request.
    - run the ab_tests
    - and the 
- Run the tests for 5 minutes.
- Stop the HTTP clients.
- Stop the VLC clients.
- Stop IFSTAT.
- Stop VLC servers.
- Stop HTTP servers.
- Stop Ryu Controller.
- Stop Mininet Topology.
- Destroy the Queue and QoS configs.

# TO DO List:
- Need to optimize the number of flows installed: currently, we have a flow installed for each source-destination pair, but we want it so that only the destination matters. Let the number of clients = C and Let the number of servers = S. Currently, we have O(C * S) flows, but we want O(C + S) flows. O(C * S) is viable for probably up to 5000 Clients and 5000 servers only.
- Make number of servers part of the topology definition.
