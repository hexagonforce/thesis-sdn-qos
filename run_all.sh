#! /usr/bin/bash

topologies=("Savvis" "Atmnet" "Ibm" "Agis" "WideJpn" "Gridnet" "Nsfnet" "Singaren" "Janetbackbone" "Canerie")
t2=("mesh" "fat_tree")

#for x in "${topologies[@]}"
#do
#    python3 change_simulate_topo.py ITZ $x
#    sudo python3 simulator.py
#    sleep 10
#done

for x in "${t2[@]}"
do
    python3 change_simulate_topo.py TOPO $x
    sudo python3 simulator.py
    sleep 10
done
