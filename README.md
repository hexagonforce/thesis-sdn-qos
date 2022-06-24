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
Remember to change the directories for `measure/run-ipstat.sh`.

First, generate the necessary pickle files and configuration files using `pkl_generator.sh`
<!--Then, run the pcap/oneway_preprocess.py to generate the correct vhost_mapping-->

Then, run `run_mininet.py` to start the Mininet topology.
Then, run the following commands to destroy the OVS-vSwitch Queues and QoS configs.
```
sudo ovs-vsctl --all destroy qos
sudo ovs-vsctl --all destroy queue
```
Then run the generated `scripts/custom/run.ovs-vsctl.case.{profile}.sh` to configure the QoSsettings on the OpenFlow OVS switches.
Then start the Ryu controller using `Controller.sh`.

# Replicating previous research with apachebenchmark and VLC
- Start the Python3 http webservers by running appropriate bash commands
- Start the VLC VOD servers by running appropriate bash commands
- Start the ifstat command with `measure/run-ipstat.sh
- Make the requests. For each client, make 1 HTTP request and 1 VLC request.
    - run the ab_tests within mininet
    - 
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
scripts/custom/switch_configs.py: 
- Don't simply assume that the "leaf switches" are the ones with higher switch dpid. Instead, use some bfs/prims to find the spanning tree and then use that tree instead for the leaf switches.
- the whole script works if we assume that each edge switch is connected to all the clients and one other switch. Otherwise, it works, but it might not choose the optimal switch based on STP.
- remember to change `config/custom/gen_config.yml`