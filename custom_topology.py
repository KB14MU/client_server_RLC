import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI

class myTopology(Topo):
    def build(self):
        # Add hosts and switches
        server = self.addHost('server', ip='10.0.0.1')
        client = self.addHost('client', ip='10.0.0.2')
        switch = self.addSwitch('s1')

        # Add links with bandwidth, delay, and loss parameters
        self.addLink(server, switch, bw=10, delay='10ms', loss=5)
        self.addLink(client, switch, bw=10, delay='10ms', loss=5)

# Dictionary of topologies with parameters
topos = {'myTopology': (lambda: myTopology())}

if __name__ == '__main__':
    topo = myTopology()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)

    # Get the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Assign scripts to hosts
    server = net.get('server')
    server_cmd = 'python {}/server.py &'.format(current_dir)
    server.cmd(server_cmd)

    # Start Mininet
    net.start()

    # Open xterm for client for manual interaction
    client = net.get('client')
    client_cmd = 'xterm -hold -e python {}/client.py &'.format(current_dir)
    client.cmd(client_cmd)

    # Enter Mininet CLI
    CLI(net)

    # Clean up
    net.stop()