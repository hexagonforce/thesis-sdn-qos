# SDN-Framework-main

This is the documentation for the SDN QoS testing framework written by Hyeong Seon Yoo, Josiah Elezar T. Regencia and William Emmanuel S. Yu.

# Configuration
Most configuration will be done in `config/class_profile_functionname.yml` and `config/simulate_topo.yml`. Refer to `example_configs/`. To get started, copy those files over to `configs/`.

## Adding custom topology
First, place in the definition for your network topology in `scripts/network_topologies.py`
Then, add in the parameters needed for the network topology in `config/simulate_topo.yml`
If you want to use your own GraphML file, the place it in the `zoo_data` directory, and change `config/simulate_topo.yml` under the `custom` data.

## Custom Configuration and Scripts
The _Load Configuration_, _Source Queue Grouping Configuration_, _Hosts Configuration_ files are generated from the class profile and topology definitions file. More specifically, they are emitted by the calling `scripts/custom/network_configs.py` script.

`scripts/custom/network_configs.py` calls the following functions that need to be defined in the `scripts/custom/networkconfig` package:

- `clients`
- `load_conf`
- `source_queue`
- `switch_configs`
- `ovs_qosgenerator`
- `hosts`

`scripts/custom/nodes_config.py` simply moves the configuration files generated to `config/custom` to a singular `json` file.

# Using the test framework
Remember to change the directories for `measure/run-ipstat.sh`.

First, generate the necessary pickle files and configuration files using `runscripts.sh`
<!--Then, run the pcap/oneway_preprocess.py to generate the correct vhost_mapping-->

Then, run `run_mininet.py` to start the Mininet topology.
Then, run `reset_qos.sh at_leaf` to reset the OVS Switch QoS settings.
Then start the Ryu controller using `Controller.sh`.

Alternatively, run `sudo python3 simulator.py` to run all the scripts and tests automatically.

`simulator.py` optionally takes an integer parameter which specifies the number of iterations.

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
