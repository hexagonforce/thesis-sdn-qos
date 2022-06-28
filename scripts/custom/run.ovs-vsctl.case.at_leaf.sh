sudo ovs-vsctl -- set Port switch17-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch17-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch17-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch18-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch18-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch19-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch19-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch19-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch19-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch20-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch20-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch20-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch21-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch21-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch21-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch22-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch22-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch22-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch22-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch23-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch23-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch23-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch23-eth5 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch23-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch24-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch24-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch25-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch25-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch2-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch2-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch2-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch3-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch3-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch3-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch3-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch4-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch4-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch5-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch5-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth5 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth6 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch7-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch7-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch8-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch8-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch9-eth4 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch9-eth5 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch9-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch9-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch10-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch11-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch12-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch13-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch14-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch14-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch15-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch16-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
