## This application is intended to emulate a client server topology in a mininet environment.
## it use UDP transport protocol and ARQ acknowledgements for reliebility.
## it include a reinforcement learning model done using tensorflow to build Deep Q-Network (DQN) algorithm.
## also some metrics and impairments was introduces as part of the emulation and to calculate the reward so the system can learn.
## The naming convention i used here are strat forward as you can understand what is the function of each script by just reading it.
## please note that the code still need some improvement to match a real transmision senario

## lets start by runing the scripts:

## Install Mininet inside linux environment or VM i used (https://mac.getutm.app/) for vertualization and ubuntu 22.04.
## Start by cloning the repo
git clone https://github.com/mininet/mininet

cd mininet

git tag  ## list available versions

git checkout -b mininet-2.3.0 2.3.0   ## or whatever version you wish to install

cd ..

mininet/util/install.sh [options]

a: install everything that is included in the Mininet VM, including dependencies like Open vSwitch as well the additions like the OpenFlow wireshark dissector and POX. By default these tools will be built in directories created in your home directory.

nfv: install Mininet, the OpenFlow reference switch, and Open vSwitch

s mydir: use this option before other options to place source/build trees in a specified directory rather than in your home directory.

## Build an environment venv

apt install python3.10-venv

python3.10 -m venv mininet_env

source mininet_env/bin/activate

## Install dependencies

pip install -r requirements.txt

### Make sure tensorflow are installed properly

pip list


## run the custom topology built for mininet that uses our server and client app

chmod +x mininet_env.sh

./mininet_env.sh


## Verify Connectivity:
## Use Mininet's pingall command to check the connectivity between different hosts in your topology.

pingall

## Open terminals for client and server using xterm and run your custom server and client scripts.

mininet> xterm client server

## make sure the venv are activated

source mininet_env/bin/activate

server python3 /home/khalid/Documents/mininet-scripts/server.py

client python3 /home/khalid/Documents/mininet-scripts/client.py

or

In client xterm: python client.py

In server xterm: python server.py

### you can use wireshark for testing
