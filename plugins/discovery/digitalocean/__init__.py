''' DigitalOcean discovery plugin '''

import time
import json
import requests
from core.discover import BaseDiscover
import core.logs

class Discover(BaseDiscover):
    ''' Main Discover Class '''

    def start(self):
        ''' Start Discovery '''
        logs = core.logs.Logger(config=self.config, proc_name="discovery.digitalocean")
        logger = logs.getLogger()
        logger = logs.clean_handlers(logger)
        logger.debug("Getting hosts from DigitalOcean")

        # Define DO information for API Request
        url = "{0}/droplets".format(self.config['discovery']['plugins']['digitalocean']['url'])
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(
                self.config['discovery']['plugins']['digitalocean']['api_key'])
        }

        while True:
            try:
                # Make http GET request and timeout after 3 seconds
                r = requests.get(url=url, headers=headers, timeout=3.0)
            except Exception as e:
                # Warn of issue and try again later
                logger.warn("Unable to query DigitalOcean API: {0}".format(e.message))
                if "unit_testing" in self.config.keys():
                    raise Exception(e.message)
                else:
                    continue

            ip_addrs = []
            if r.status_code == 200:
                try:
                    response = json.loads(r.text)
                except ValueError:
                    # If we got bad json assume it's empty
                    response = {}

                if "droplets" in response.keys():
                    for droplet in response['droplets']:
                        for ip_type in ['v4', 'v6']:
                            for interface in droplet['networks'][ip_type]:
                                if interface['type'] == "public":
                                    logger.debug("Found host: {0}".format(interface['ip_address']))
                                    ip_addrs.append(interface['ip_address'])
            else:
                logger.warn("Unable to query DigitalOcean API: HTTP Response {0}".format(r.status_code))

            for ip in ip_addrs:
                if self.dbc.new_discovery(ip=ip):
                    logger.debug("Added host {0} to discovery queue".format(ip))
                else:
                    logger.debug("Failed to add host {0} to discovery queue".format(ip))

            logger.info("Found {0} hosts".format(len(ip_addrs)))
            if "unit_testing" in self.config.keys():
                # Break out of loop for unit testing
                break
            else:
                time.sleep(self.config['discovery']['plugins']['digitalocean']['interval'])
        # Return true for unit testing
        return True
