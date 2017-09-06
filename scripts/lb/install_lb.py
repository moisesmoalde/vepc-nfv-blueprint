
import socket
import struct

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify import exceptions
from cloudify import utils


def run(command, errorMessage):
    runner = utils.LocalCommandRunner(logger=ctx.logger)
    try:
        runner.run(command)
    except exceptions.CommandExecutionException as e:
        raise exceptions.NonRecoverableError('{0}: {1}'.format(
                errorMessage, e))

def cidrToNetmask(cidr):
	hostBits = 32 - int(cidr.split("/")[1])
	return socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << hostBits)))


VIP = str(inputs["virtual_ip"])
NETWORK = str(inputs["network"]).split("/")[0]
NETMASK = cidrToNetmask(str(inputs["network"]))

ctx.logger.info("Update the APT software")
run("sudo apt-get -y update", "Error updating APT software")

ctx.logger.info("Installing ipvsadm Linux Virtual Server administration packages for load balancing")
run("sudo DEBIAN_FRONTEND=noninteractive apt-get install ipvsadm --yes --force-yes",
	errorMessage = "Error while trying to install ipvsadm")

ctx.logger.info("Editing ipvsadm configuration")
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

ctx.logger.info("Setting virtual IP runtime property")
ctx.instance.runtime_properties['virtual_ip'] = VIP

ctx.logger.info("Set up eth0:0 interface")
run("sudo ifup eth0:0", "Error setting up eth0:0 interface")

ctx.logger.info("LB successfully installed and configured")
