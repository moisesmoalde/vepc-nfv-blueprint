import os
import subprocess

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

MME_DIR = ctx.instance.runtime_properties["mme_dir"]
MME_IP = inputs["ip"] # Private IP
RAN_IP = inputs["ran_ip"]
HSS_IP = inputs["hss_ip"]
SGW_IP = inputs["sgw_ip"]
PGW_IP = inputs["pgw_ip"]
S1_THREADS = inputs["s1_mme_threads"]
CMD = ["nohup",
		MME_DIR + "/src/mme.out",
		S1_MME_THREADS,
		MME_IP,
		RAN_IP,
		HSS_IP,
		SGW_IP,
		PGW_IP]


ctx.logger.info("Running MME node")
with open(os.devnull, 'wb') as dn:
	process = subprocess.Popen(CMD, stdout=dn, stderr=dn)


ctx.logger.info('Setting PID runtime property: {0}'.format(process.pid))
ctx.instance.runtime_properties['pid'] = process.pid
