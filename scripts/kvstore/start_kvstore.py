import os
import subprocess

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs


SOCKET_ADDR = str(inputs["socket_address"] or "127.0.0.1:8090")

CMD = ["$GOPATH/src/levelmemdb/go", "run", "server.go", SOCKET_ADDR]

ctx.logger.info(" ".join(CMD))

ctx.logger.info("Running KVStore node")
with open(os.devnull, 'wb') as dn:
	process = subprocess.Popen(CMD, stdout=dn, stderr=dn)


ctx.logger.info('Setting PID runtime property: {0}'.format(process.pid))
ctx.instance.runtime_properties['pid'] = process.pid
