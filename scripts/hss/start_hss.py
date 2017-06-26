import os
import subprocess

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

HSS_DIR = ctx.instance.runtime_properties["hss_dir"]
HSS_IP = ctx.instance.runtime_properties["ip"] # Private IP
S6A_THREADS = inputs["s6a_threads"]
CMD = ["nohup", HSS_DIR + "/src/hss.out", S6A_THREADS, HSS_IP]


ctx.logger.info("Running HSS node")
with open(os.devnull, 'wb') as dn:
	process = subprocess.Popen(CMD, stdout=dn, stderr=dn)


ctx.logger.info('Setting PID runtime property: {0}'.format(process.pid))
ctx.instance.runtime_properties['pid'] = process.pid
