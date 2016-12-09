''' Roster file discovery plugin '''

import time
import json
import requests
from core.discover import BaseDiscover
import core.logs

class Discover(BaseDiscover):
    ''' Main Discover Class '''

    def start(self):
        ''' Start Discovery '''
        logs = core.logs.Logger(config=self.config, proc_name="discovery.roster")
        logger = logs.getLogger()
        logger = logs.clean_handlers(logger)
        logger.debug("Getting hosts from Roster")

        while True:
            found = []
            try:
                for ip in self.config['discovery']['plugins']['roster']['hosts']:
                    found.append(ip)
                    if self.dbc.new_discovery(ip=ip):
                        logger.debug("Added host {0} to discovery queue".format(ip))
                    else:
                        logger.debug("Failed to add host {0} to discovery queue".format(ip))
            except KeyError as e:
                logger.warn("Configuration syntax error: {0}".format(e.message))

            logger.info("Found {0} hosts".format(len(found)))
            if "unit_testing" in self.config.keys():
                # Break out of loop for unit testing
                break
            else:
                # Adding sleep() so master process doesn't exit after completion
                time.sleep(900)
        # Return true for unit testing
        return True
