import os
import subprocess

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

PGW_DIR = ctx.instance.runtime_properties["pgw_dir"]
PGW_IP = inputs["ip"] # Private IP
SGW_IP = inputs["sgw_ip"]
SINK_IP = inputs["sink_ip"]
S5_THREADS = inputs["s5_threads"]
SGI_THREADS = inputs["sgi_threads"]
CMD = ["nohup",
		PGW_DIR + "/src/pgw.out",
		S5_THREADS,
		SGI_THREADS,
		PGW_IP,
		SGW_IP,
		SINK_IP]


ctx.logger.info("Running PGW node")
with open(os.devnull, 'wb') as dn:
	process = subprocess.Popen(CMD, stdout=dn, stderr=dn)


ctx.logger.info('Setting PID runtime property: {0}'.format(process.pid))
ctx.instance.runtime_properties['pid'] = process.pid
