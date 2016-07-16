''' Syslog logging handler '''

import logging
import logging.handlers
import sys
from core.logs import BaseLogging

class Logger(BaseLogging):
    ''' Handler class for Syslog Logging '''

    def setup(self):
        ''' Setup class for handler '''
        lh = logging.handlers.SysLogHandler(
            facility=self.config['logging']['plugins']['syslog']['facility'])
        lh.setLevel(logging.DEBUG)
        logfmt = logging.Formatter("%(name)s[%(process)d] - %(levelname)s - %(message)s")
        lh.setFormatter(logfmt)
        return lh
