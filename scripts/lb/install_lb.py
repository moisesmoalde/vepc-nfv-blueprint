import os
import subprocess
from subprocess import STDOUT, check_call
import socket
import struct

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

def cidrToNetmask(cidr):
	hostBits = 32 - int(cidr.split("/")[1])
	return socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << hostBits)))

VIP = str(inputs["virtual_ip"])
NETWORK = str(inputs["network"]).split("/")[0]
NETMASK = cidrToNetmask(str(inputs["network"]))

ctx.logger.info("Update the APT software")
check_call(['sudo', 'apt-get', '-y', 'update'],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)

ctx.logger.info("Installing ipvsadm Linux Virtual Server administration packages for load balancing")
check_call(['sudo', 'DEBIAN_FRONTEND=noninteractive', 'apt-get', 'install', 'ipvsadm', '--yes', '--force-yes'],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)

ctx logger info "Editing ipvsadm configuration"
ipvsadmConfFile = open("/etc/default/ipvsadm", "w")
ipvsadmConfFile.write('# ipvsadm configuration\n\n')
ipvsadmConfFile.write('# if you want to start ipvsadm on boot set this to true\n')
ipvsadmConfFile.write('AUTO="true"\n\n')
ipvsadmConfFile.write('# daemon method (none|master|backup)\n')
ipvsadmConfFile.write('DAEMON="master"\n\n')
ipvsadmConfFile.write('# use interface (eth0,eth1...)\n')
ipvsadmConfFile.write('IFACE="eth0"\n\n')
ipvsadmConfFile.write('# syncid to use\n')
ipvsadmConfFile.write('SYNCID="1"\n\n')
ipvsadmConfFile.write('auto eth0:0\n')
ipvsadmConfFile.write('iface eth0:0 inet static\n')
ipvsadmConfFile.write('address ' + VIP + '\n')
ipvsadmConfFile.write('network ' + NETWORK + '\n')
ipvsadmConfFile.write('netmask ' + NETMASK + '\n')
ipvsadmConfFile.close()

ctx.logger.info("Set up eth0:0 interface")
check_call(['sudo', 'ifup', 'eth0:0'],
     stdout=open(os.devnull,'wb'), stderr=STDOUT)

ctx logger info "LB successfully installed and configured"
