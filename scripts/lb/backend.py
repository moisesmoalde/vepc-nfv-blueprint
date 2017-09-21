
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


VIP = str(ctx.target.instance.runtime_properties.get('virtual_ip'))

ctx.logger.info("Adding iptables entry for self-redirecting traffic")
run("sudo iptables -t nat -A PREROUTING -d {0} -j REDIRECT".format(VIP),
	errorMessage = "Iptables entry failed to being inserted")

ctx.logger.info("Load balancing setup complete at backend server")
