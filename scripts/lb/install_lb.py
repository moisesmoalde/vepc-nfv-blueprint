
import socket
import struct

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify import exceptions
from cloudify import utils


def run(command, errorMessage = "Error"):
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
run("sudo printf '# ipvsadm configuration\n\n' > /etc/default/ipvsadm")
run("sudo printf '# if you want to start ipvsadm on boot set this to true\n' >> /etc/default/ipvsadm")
run("sudo printf 'AUTO=\"true\"\n\n' >> /etc/default/ipvsadm")
run("sudo printf '# daemon method (none|master|backup)\n' >> /etc/default/ipvsadm")
run("sudo printf 'DAEMON=\"master\"\n\n' >> /etc/default/ipvsadm")
run("sudo printf '# use interface (eth0,eth1...)\n' >> /etc/default/ipvsadm")
run("sudo printf 'IFACE=\"eth0\"\n\n' >> /etc/default/ipvsadm")
run("sudo printf '# syncid to use\n' >> /etc/default/ipvsadm")
run("sudo printf 'SYNCID=\"1\"\n\n' >> /etc/default/ipvsadm")
run("sudo printf 'auto eth0:0\n' >> /etc/default/ipvsadm")
run("sudo printf 'iface eth0:0 inet static\n' >> /etc/default/ipvsadm")
run("sudo printf 'address {0}\n' >> /etc/default/ipvsadm".format(VIP))
run("sudo printf 'network {0}\n' >> /etc/default/ipvsadm".format(NETWORK))
run("sudo printf 'netmask {0}\n' >> /etc/default/ipvsadm".format(NETMASK))

ctx.logger.info("Setting virtual IP runtime property")
ctx.instance.runtime_properties['virtual_ip'] = VIP

ctx.logger.info("Set up eth0:0 interface")
run("sudo ifup eth0:0", "Error setting up eth0:0 interface")

ctx.logger.info("LB successfully installed and configured")
