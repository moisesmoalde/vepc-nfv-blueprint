import os
import subprocess

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

SGW_DIR = ctx.instance.runtime_properties["sgw_dir"]
#SGW_IP = str(inputs["ip"]) # Private IP
SGW_IP = ctx.instance.host_ip
S11_THREADS = str(inputs["s11_threads"])
S1_U_THREADS = str(inputs["s1_u_threads"])
S5_THREADS = str(inputs["s5_threads"])
CMD = [SGW_DIR + "/src/sgw.out",
		S11_THREADS,
		S1_U_THREADS,
		S5_THREADS,
		SGW_IP]
ctx.logger.info(" ".join(CMD))

ctx.logger.info("Running SGW node")
with open(os.devnull, 'wb') as dn:
	process = subprocess.Popen(CMD, stdout=dn, stderr=dn)


ctx.logger.info('Setting PID runtime property: {0}'.format(process.pid))
ctx.instance.runtime_properties['pid'] = process.pid
