#!/bin/bash

# Activate your Python virtual environment
source mininet_env/bin/activate

# Launch Mininet console
sudo mn --custom custom_topology.py --topo=myTopology --controller=ovsc --switch ovsk,protocols=OpenFlow13
