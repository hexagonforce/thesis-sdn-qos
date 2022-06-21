#! /usr/bin/bash
sudo ovs-vsctl --all destroy qos
sudo ovs-vsctl --all destroy queue
./scripts/custom/run.ovs-vsctl.case.$1.sh