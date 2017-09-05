
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
                error_message, e))


VIP = str(inputs["virtual_ip"])
PORTS = [str(port) for (key, port) in inputs.items() if key is not "virtual_ip"]

for port in PORTS:
	run("ipvsadm -A -u {0}:{1} -s sh".format(VIP, port),
		errorMessage = "Failed trying to add a new load balancing virtual service")

ctx.logger.info("Running load balancer with VIP {0}".format(VIP))
