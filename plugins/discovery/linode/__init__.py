''' Linode discovery plugin '''

import time
import json
import requests
from core.discover import BaseDiscover
import core.logs

class Discover(BaseDiscover):
    ''' Main Discover Class '''

    def start(self):
        ''' Start Discovery '''
        logs = core.logs.Logger(config=self.config, proc_name="discovery.linode")
        logger = logs.getLogger()
        logger = logs.clean_handlers(logger)
        logger.info("Getting hosts from Linode")

        # Define Linode information for API Request
        url = "{0}/".format(self.config['discovery']['plugins']['linode']['url'])
        params = {
            'api_key': '{0}'.format(self.config['discovery']['plugins']['linode']['api_key']),
            'api_action': 'linode.ip.list'
        }

        while True:
            try:
                # Make http GET request and timeout after 3 seconds
                r = requests.get(url=url, params=params, timeout=3.0)
            except Exception as e:
                # Warn of issue and try again later
                logger.warn("Unable to query Linode API: {0}".format(e.message))
                if "unit_testing" in self.config.keys():
                    raise Exception(e.message)
                else:
                    continue

            ip_addrs = []
            if r.status_code >= 200 and r.status_code <= 300:
                try:
                    response = json.loads(r.text)
                except ValueError:
                    # If we got bad json assume it's empty
                    response = {'DATA': []}

                for node in response['DATA']:
                    logger.debug("Found host: {0}".format(node['IPADDRESS']))
                    ip_addrs.append(node['IPADDRESS'])
            else:
                logger.warn("Unable to query Linode API: HTTP Response {0}".format(r.status_code))

            for ip in ip_addrs:
                if self.dbc.new_discovery(ip=ip):
                    logger.debug("Added host {0} to discovery queue".format(ip))
                else:
                    logger.debug("Failed to add host {0} to discovery queue".format(ip))

            logger.debug("Found {0} hosts".format(len(ip_addrs)))
            if "unit_testing" in self.config.keys():
                # Break out of loop for unit testing
                break
            else:
                time.sleep(self.config['discovery']['plugins']['linode']['interval'])
        # Return true for unit testing
        return True
