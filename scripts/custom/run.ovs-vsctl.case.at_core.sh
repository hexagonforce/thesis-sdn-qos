sudo ovs-vsctl -- set Port switch1-eth9 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
sudo ovs-vsctl -- set Port switch6-eth1 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=0 -- --id=@q1 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=1 -- --id=@q2 create Queue other-config:min-rate=333333334 other-config:max-rate=333333334 other-config:priority=2
