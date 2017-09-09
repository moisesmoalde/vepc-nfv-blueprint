
# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs
from cloudify import exceptions
from cloudify import utils

ADD_MESSAGE = "Adding a real server to a virtual service"
RM_MESSAGE = "Removing a real server from a virtual service"

def run(command, errorMessage):
    runner = utils.LocalCommandRunner(logger=ctx.logger)
    try:
        runner.run(command)
    except exceptions.CommandExecutionException as e:
        raise exceptions.NonRecoverableError('{0}: {1}'.format(
                errorMessage, e))

def addBackend(virtual_ip = None, portList = None, backendAddress = None, add = True):
	vip = virtual_ip or ctx.target.instance.runtime_properties.get('virtual_ip')
	ports = portList or ctx.target.node.properties['ports']
	ip = backendAddress or ctx.source.instance.host_ip
	ctx.logger.info(ADD_MESSAGE if add else RM_MESSAGE)
	for port in str(ports).split(","):
		run("sudo ipvsadm -{0} -u {1}:{2} -r {3}:{4}"
			.format(("a" if add else "d"), str(vip), port, str(ip), port),
			"Error -> {0}".format(ADD_MESSAGE if add else RM_MESSAGE))

def removeBackend(vip = None, portList = None, backendAddress = None):
	addBackend(vip, portList, backendAddress, False)

def main():
	invocation = inputs['invocation']
	function = invocation['function']
	args = invocation.get('args', [])
	kwargs = invocation.get('kwargs', {})
	globals()[function](*args, **kwargs)


if __name__ == '__main__':
	main()
