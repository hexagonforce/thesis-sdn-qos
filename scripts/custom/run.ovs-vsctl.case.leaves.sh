sudo ovs-vsctl -- set Port switch1-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch1-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch1-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch3-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch3-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch3-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch3-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch4-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch4-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch4-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch5-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch5-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch5-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth5 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch7-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch7-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch7-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch8-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch8-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch8-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch9-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch9-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch9-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch10-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch10-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch10-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth9 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth10 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth11 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth5 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth6 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth7 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth8 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch12-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch12-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch12-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch13-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch13-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch13-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
