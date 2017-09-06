
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

def addBackend(virtual_ip = None, portList = None, backendAddress = None, add = True):
	vip = virtual_ip or ctx.target.instance.runtime_properties.get('virtual_ip')
	ports = portList or ctx.target.node.properties['ports']
	ip = backendAddress or ctx.source.instance.host_ip
	for port in str(ports).split(","):
		run("sudo ipvsadm -{0} -u {1}:{2} -r {3}:{4} -g".format(("a" if add else "d"), str(vip), port, str(ip), port),
			"Error adding a real server to a virtual service" if add else
			"Error removing a real server from a virtual service")

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
