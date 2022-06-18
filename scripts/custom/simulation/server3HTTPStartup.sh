#!/bin/bash
cd
cd server3
# iperf3 -s -p 5566 -i 1 &
sudo python3 -m http.server 80 --bind 10.0.1.103
