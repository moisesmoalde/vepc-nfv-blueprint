import os
import subprocess
import signal

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

def addBackend(backendAddress = None, add = True):
	backend_id = ctx.source.instance.id
	ip = backendAddress or ctx.source.instance.host_ip
	ctx.logger.info(ADD_MESSAGE if add else RM_MESSAGE)

	backends = ctx.target.instance.runtime_properties.get('backends', {})
	if add:
		backends[backend_id] = ip
	else:
		backends.pop(backend_id, None)
	ctx.target.instance.runtime_properties['backends'] = backends
	lbUpdate(backends)
	ctx.target.instance.update()
	ctx.logger.info("Updated backends to: " + str(backends))


def removeBackend(backendAddress = None):
	addBackend(backendAddress, False)

def lbUpdate(backends):
	ports = ctx.target.instance.runtime_properties.get('ports', {})

	if not backends.values():
		ctx.target.instance.runtime_properties['ports'] = dict([(port, None) for port in ports.keys()])
		return

	for port, pid in ports.iteritems():
		if pid is not None: os.kill(int(pid), signal.SIGTERM)
		CMD = ["pen", "-Ur", port] + [str(ip) for ip in backends.values()]
		with open(os.devnull, 'wb') as dn:
			process = subprocess.Popen(CMD, stdout=dn, stderr=dn)
		ports[port] = process.pid+2

	ctx.target.instance.runtime_properties['ports'] = ports
	ctx.logger.info("Updated pids to: " + str(ports))


def main():
	invocation = inputs['invocation']
	function = invocation['function']
	args = invocation.get('args', [])
	kwargs = invocation.get('kwargs', {})
	globals()[function](*args, **kwargs)


if __name__ == '__main__':
	main()
