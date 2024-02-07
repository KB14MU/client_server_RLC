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
        """Create a Mininet network with a custom topology"""
        net = Mininet(controller=OVSController, link=TCLink)
        info('*** Adding controller\n')
        net.addController('c0')
        info('*** Adding hosts\n')

        # Use custom Python scripts as hosts
        h1 = net.addHost('h1', ip='10.0.0.1', privateDirs=['/root/mininet-scripts'])
        h2 = net.addHost('h2', ip='10.0.0.2', privateDirs=['/root/mininet-scripts'])

        # Copy client.py and server.py to the hosts' private directories
        h1.cmd('cp /root/mininet-scripts/client.py /root/mininet-scripts')
        h2.cmd('cp /root/mininet-scripts/server.py /root/mininet-scripts')

        info('*** Adding switch\n')
        s1 = net.addSwitch('s1')
        info('*** Creating links\n')

        # Add links with different RTT, BW, and PLR
        net.addLink(h1, s1, delay='20ms', bw=10, loss=2)  # Adjust units if needed
        net.addLink(h2, s1, delay='10ms', bw=10, loss=1)  # Adjust units if needed

        return net

def main():
    setLogLevel('info')
    topology = CustomTopo()
    net = topology.build()
    
    # Set CPU limit for Mininet
    net.setCpuLimit(0.1)  # Adjust this value as needed
    
    net.start()

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