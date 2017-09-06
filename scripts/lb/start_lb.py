
# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify import exceptions
from cloudify import utils


def run(command, errorMessage):
    runner = utils.LocalCommandRunner(logger=ctx.logger)
    try:
        runner.run(command)
    except exceptions.CommandExecutionException as e:
        raise exceptions.NonRecoverableError('{0}: {1}'.format(
                errorMessage, e))


VIP = str(ctx.instance.runtime_properties['virtual_ip'])
PORTS = str(ctx.node.properties["ports"]).split(",")

for port in PORTS:
	run("ipvsadm -A -u {0}:{1} -s sh".format(VIP, port),
		errorMessage = "Failed trying to add a new load balancing virtual service")

ctx.logger.info("Running load balancer with VIP {0}".format(VIP))
