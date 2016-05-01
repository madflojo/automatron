''' Logging Module '''

import logging
import logging.handlers

class BaseLogging(object):
    ''' Base class for plugins to import '''

    def __init__(self, config=None, proc_name=None):
        ''' Initialize '''
        self.config = config
        self.proc_name = proc_name


    def setup(self):
        ''' Set up logging handler '''
        pass


class Logger(BaseLogging):
    ''' Class for adding log handlers '''

    def getLogger(self):
        ''' Initialize and load log handlers '''

        logger = logging.getLogger(self.proc_name)
        logger.setLevel(logging.INFO)
        if "debug" in self.config['logging']:
            if self.config['logging']['debug']:
                logger.setLevel(logging.DEBUG)

        # Load and add a handler for each logging mechanism
        for loghandler in self.config['logging']['plugins'].keys():
            plugin = __import__("plugins.logging." + loghandler, globals(),
                                locals(), ['Logger'], -1)
            lh = plugin.Logger(config=self.config, proc_name=self.proc_name)
            logger.addHandler(lh.setup())

        return logger

    def clean_handlers(self, logger):
        ''' Remove handlers from logger for threads '''
        while len(logger.handlers) > 0:
            logger.removeHandler(logger.handlers[0])
        return logger
