#!/bin/bash

python3 scripts/network_topologies.py
for file in scripts/custom/*.py; 
do
	python3 "$file"; 
	if [[ $? -ne 0 ]]; then
		break
	fi
done
