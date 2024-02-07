import os
import time
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo

class CustomTopo(Topo):
    def build(self):
        """Custom topology with an existing Mininet network."""
        info('*** Adding controller\n')
        self.addController('c0')
        info('*** Adding hosts\n')

        # Use custom Python scripts as hosts
        h1 = self.addHost('h1', ip='10.0.0.1', privateDirs=['/root'])
        h2 = self.addHost('h2', ip='10.0.0.2', privateDirs=['/root'])

        # Copy client.py and server.py to the hosts' private directories
        h1.cmd('cp /root/mininet-scripts/client.py /root')
        h2.cmd('cp /root/mininet-scripts/server.py /root')

        info('*** Adding switch\n')
        s1 = self.addSwitch('s1')
        info('*** Creating links\n')

        # Add links with different RTT, BW, and PLR
        self.addLink(h1, s1, intfName1='h1-eth0-custom', intfName2='s1-eth1-custom', delay='20ms', bw=10, loss=2)
        self.addLink(h2, s1, intfName1='h2-eth0-custom', intfName2='s1-eth2-custom', delay='20ms', bw=10, loss=1)

        return net

def main():
    setLogLevel('info')
    net = Mininet(controller=OVSController, link=TCLink)
    topology = CustomTopo()
    topology.build(net)
    
    # Set CPU limit for Mininet
    net.setCpuLimit(0.1)  # Adjust this value as needed
    
    net.start()

    # Connect the controller to the switches
    s1 = net.get('s1')
    c0 = net.getController('c0')
    net.addLink(s1, c0)

    # Run your server script on the server host
    server = net.get('h1')
    server.cmd('python /root/mininet-scripts/server.py &')

    # Run your client script on the client host
    client = net.get('h2')
    client.cmd('python /root/mininet-scripts/client.py &')

    CLI(net)  # Start the Mininet CLI for testing
    net.stop()

if __name__ == '__main__':
    main()