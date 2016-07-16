''' Console Logging Handler '''

import logging
import logging.handlers
from core.logs import BaseLogging

class Logger(BaseLogging):
    ''' Logging Class '''

    def setup(self):
        ''' Setup logging handler '''
        lh = logging.StreamHandler()
        lh.setLevel(logging.DEBUG)
        lf = logging.Formatter("%(asctime)s - %(name)s[%(process)d] - %(levelname)s - %(message)s")
        lh.setFormatter(lf)
        return lh
