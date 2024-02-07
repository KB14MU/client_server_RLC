import os
import time
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.node import RemoteController

class CustomTopo(Topo):
    def build(self):
        """Custom topology with an existing Mininet network."""
        info('*** Adding hosts\n')

        # Use custom Python scripts as hosts
        h1 = self.addHost('h1', ip='10.0.0.1', cls=Host, privateDirs=['/root'])
        h2 = self.addHost('h2', ip='10.0.0.2', cls=Host, privateDirs=['/root'])

        info('*** Adding switch\n')
        # Assigning a name to the switch
        s1 = self.addSwitch('s1')
        info('*** Creating links\n')

        # Add links with different RTT, BW, and PLR
        self.addLink(h1, s1, intfName1='h1-eth0-custom', intfName2='s1-eth1-custom', delay='20ms', bw=10, loss=2)
        self.addLink(h2, s1, intfName1='h2-eth0-custom', intfName2='s1-eth2-custom', delay='20ms', bw=10, loss=1)

        return s1  # Return the reference to switch 's1'

def main():
    setLogLevel('info')

    # Start the controller (POX with OpenFlow 1.0)
    controller_cmd = "/home/khalid/Documents/pox/pox.py --verbose openflow.of_01 --port=6633 forwarding.l2_learning &"
    os.system(controller_cmd)

    # Add a delay to allow the controller to start
    time.sleep(10)

    # Create Mininet object
    net = Mininet(link=TCLink)

    # Build the topology
    topology = CustomTopo()
    s1 = topology.build()

    # Start Mininet
    net.start()

    # Print the list of nodes in the network
    print("Nodes in the network:", net.controllers, net.switches, net.hosts)

    # Ensure the switch is named 's1'
    if s1 is not None:
        info(f"Switch 's1' is found.\n")
    else:
        info("Switch 's1' not found.\n")

    # Add controller to the switch
    controller_ip = "127.0.0.1"
    controller_port = 6633
    net.addController('c0', controller=RemoteController, ip=controller_ip, port=controller_port)

    # Run your server script on the server host
    server = net.get('h1')
    if server is not None:
        info(f"Host 'h1' is found.\n")
        server.cmd('python /root/mininet-scripts/server.py &')
    else:
        info("Host 'h1' not found.\n")

    # Run your client script on the client host
    client = net.get('h2')
    if client is not None:
        info(f"Host 'h2' is found.\n")
        client.cmd('python /root/mininet-scripts/client.py &')
    else:
        info("Host 'h2' not found.\n")

    CLI(net)  # Start the Mininet CLI for testing
    net.stop()

if __name__ == '__main__':
    main()
