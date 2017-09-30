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
run("sudo DEBIAN_FRONTEND=noninteractive apt-get install unzip --yes --force-yes")
run("sudo mkdir -p /tmp/vepc-nfv-blueprint-master")

ctx.logger.info("Installing pen package with dependencies for load balancing")
run("wget https://github.com/moisesmoalde/vepc-nfv-blueprint/archive/master.zip -O /tmp/vepc-nfv-blueprint-master.zip",
	errorMessage = "Error downloading vepc-nfv-blueprint")
run("sudo unzip /tmp/vepc-nfv-blueprint-master.zip -d /tmp")

run("sudo dpkg -i /tmp/vepc-nfv-blueprint-master/scripts/lb/libssl1.1_1.1.0f-3_amd64.deb",
	errorMessage = "Error installing libssl1.1 library")
run("sudo dpkg -i /tmp/vepc-nfv-blueprint-master/scripts/lb/pen_0.34.1-1_amd64.deb",
	errorMessage = "Error installing pen package")

ctx.logger.info("Enabling IPv4 forwarding")
run('sudo sysctl -w net.ipv4.ip_forward=1', "Error enabling IPv4 forwarding")

ctx.logger.info("Setting ports dictionary runtime property for storing PIDs")
ctx.instance.runtime_properties['ports'] = dict([(port, None) for port in PORTS])

ctx.logger.info("LB successfully installed and configured")
