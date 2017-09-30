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

PORTS = str(ctx.node.properties["ports"]).split(",")

ctx.logger.info("Update the APT software")
run("sudo apt-get -y update", "Error updating APT software")

ctx.logger.info("Installing pen package with dependencies for load balancing")
run("wget http://ftp.us.debian.org/debian/pool/main/o/openssl/libssl1.1_1.1.0f-3_amd64.deb",
	errorMessage = "Error downloading libssl1.1 library")
run("sudo dpkg -i libssl1.1_1.1.0f-3_amd64.deb",
	errorMessage = "Error installing libssl1.1 library")
run("wget http://ftp.us.debian.org/debian/pool/main/p/pen/pen_0.34.1-1_amd64.deb",
	errorMessage = "Error downloading pen package")
run("sudo dpkg -i pen_0.34.1-1_amd64.deb",
	errorMessage = "Error installing pen package")

ctx.logger.info("Enabling IPv4 forwarding")
run('sudo sysctl -w net.ipv4.ip_forward=1', "Error enabling IPv4 forwarding")

ctx.logger.info("Setting ports dictionary runtime property for storing PIDs")
ctx.instance.runtime_properties['ports'] = dict([(port, None) for port in PORTS])

ctx.logger.info("LB successfully installed and configured")
