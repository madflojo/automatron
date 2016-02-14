''' Console Logging Handler '''

from core.logs import BaseLogging
import logging
import logging.handlers

class Logger(BaseLogging):
    ''' Logging Class '''

    def setup(self):
        ''' Setup logging handler '''
        lh = logging.StreamHandler()
        lh.setLevel(logging.DEBUG)
        lf = logging.Formatter("%(asctime)s - %(name)s[%(process)d] - %(levelname)s - %(message)s")
        lh.setFormatter(lf)
        return lh
