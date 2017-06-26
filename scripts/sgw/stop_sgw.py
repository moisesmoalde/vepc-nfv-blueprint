import os
import signal

# Import Cloudify's context object.
# This provides several useful functions as well as allowing to pass
# contextual information of an application.
from cloudify import ctx

# Here, we read the `pid` runtime property which we previously
# saved when running `install.py`
pid = ctx.instance.runtime_properties['pid']
ctx.logger.info('Running process PID: {0}'.format(pid))

try:
    os.kill(pid, signal.SIGTERM)
    ctx.logger.info('SGW node stopped')
except:
    ctx.logger.info('SGW node not running')
